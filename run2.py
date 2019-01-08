import mf2
import mods
import sys
import subprocess
import multiprocessing as mp
import time
import gmtfuncs
import threading

#this script relies on gmt-python. To install, please follow the directions given here: https://www.gmtpython.xyz/latest/install.html
#it also requires ffmpeg, which should come with any unix OS
#the other files will not need to be changed, except for possibly the polygon directory in gmtfuncs.py, in the plot_prep function
#you may also want to add/change a model. This can be done in mods.py

sd = mf2.station_dict() #where all the stations are located
ver = sys.argv[1] #run2.py is argv[0], this determines the file name of the input and output - comment if you want to adjust it manually
framedirn = sys.argv[2] #the framedir is where the frames will be saved
mediacom = "mpv --keep-open" #chose a command for a media player to open the video after you've made it
cores = mp.cpu_count() #how many cores to use? set to mp.cpu_count() to let python use the maximum

#mod = "Cascadia" #the model - see mods.py for the associated model parameters
mod = "Tohoku"
f = 'movie/inputs/{}{}.d'.format(mod, ver) #what file is going to be plotted
print("reading from this file:", f)
mov_name = "movie/outputs/{}-mov-{}.mp4".format(mod, ver) #where the movie will be saved
framedir = "movie/frames{}".format(framedirn) #where to save the frames


scalelat = 32.6 #where to put the scale vector - I'll try to automate this at some point
scalelon = 134.2 

#cascadia - 46.4 233.2

#---------- the lines below this point should not be changed ------------------------------------------------------------------

#---------- some preparation for other scripts ------------------------------------------------------------------
minline, maxline, reg, proj, scale, ot, mag = mods.get_mod_pars(mod)
maxslip = mf2.max_slip(f, minline, maxline)
tmqs = mf2.gen_tmq(f, minline, maxline) 
#---------------------------------------------------------------------------------------------------------------

#--------- these lines remove the old pngs in the frame directory, so nothing extra will be added to the movie
cleancom = "rm -f {}/*.png".format(framedir)
r = subprocess.check_output(cleancom,shell=True) 
#---------------------------------------------------------------------------------------------------------------

#--------- these lines generate the labels ---------------------------------------------------------------------
for i in range(0, maxline-minline):
	mf2.labeler(maxslip, mag, minline, framedir, i + minline, framedir)
#---------------------------------------------------------------------------------------------------------------

#---------- these lines plot the maps --------------------------------------------------------------------------
def caller(i, f=f, sd=sd, maxslip=maxslip, reg=reg, proj=proj, scale=scale, framedir=framedir, scalelat=scalelat, scalelon=scalelon):
	gmtfuncs.plot_fun(f, i, sd, maxslip, reg, proj, scale, "png", framedir, scalelat, scalelon)

with mp.Pool(cores) as p:
	a = p.map(caller,[x for x in range(minline, maxline)])	

# for i in range(minline, maxline):
# 	caller(i)

#---------------------------------------------------------------------------------------------------------------

#-------- these lines turn the frames into a movie
movie_com = """ffmpeg -framerate 5 -pattern_type glob -i '{1}/mov-test*.png' -vcodec libx264 -vf scale=1000:-2,format=yuv420p {0}
	{2} {0}""".format(mov_name, framedir, mediacom) #throws the pngs into a movie
b = subprocess.check_output(movie_com,shell=True)
#---------------------------------------------------------------------------------------------------------------