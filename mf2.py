from math import sin, cos, sqrt, atan2, radians, acos
import math
import numpy as np
import glob
import linecache as lc
import pkg_resources
#pkg_resources.require("matplotlib==2.0.2")
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import colors
from matplotlib.patches import Rectangle

# from matplotlib.figure import Figure
# from matplotlib.patches import Rectangle
import datetime #for converting epoch timestamps to ymdhms


def labeler(maxslip, mag, ET, tmq, n, imdir): #generates a label 
	print("generating label", n)
	cmap = matplotlib.cm.get_cmap('jet')
	fig = plt.figure(figsize=(4, 4))
	ax2 = fig.add_axes([0.05, 0.20, 0.9, 0.15])
	norm = matplotlib.colors.Normalize(vmin=0, vmax=maxslip)
	cb1 = matplotlib.colorbar.ColorbarBase(ax2, cmap=cmap,
                                norm=norm,
                                orientation='horizontal')
	cb1.set_label('Slip (meters)', fontsize=18) #label for the colorbar
	fig.text(0.3, 0.45, '0.5 meters', fontsize=18) #label for the scale vector
	extra = Rectangle((0, 0), 5, 5, fc="w", fill=False, edgecolor='none', linewidth=0)
	#fig.legend([extra], ("My explanatory text\nIs more than 1 line"), loc="lower center", ncol=50, fontsize=10) #
	#fig.text(0, 0, 'Blue lines: Measured Offsets\nRed Lines: Predicted Offsets\nEarthquake Occured At: {0}\nCurrently: {1}\nRecorded magnitude: {2}\nCalculated Magnitude: {3}\nQuality value: {4}\n'.format(ET, tmq[0], mag, tmq[1], tmq[2]), fontsize=18)
	#fig.text(0, 0, 'Blue lines: Measured Offsets\nRed Lines: Predicted Offsets\nRecorded magnitude: {2}\nCalculated Magnitude: {3}\n'.format(ET, tmq[0], mag, tmq[1], tmq[2]), fontsize=18)
	#fig.text(0, 0, 'Blue lines: Measured Offsets\n')
	plt.savefig('{}/lab{}.png'.format(imdir, n), transparent=True)
	plt.close(fig)

def reader(fi, li, e): #opens the input files. 0 as 3rd argument gets you the line as it is, 1 returns eval(line), to convert script outputs to dictionaries
	line = lc.getline(fi, li)
	if line is None:
		pass
	else:
		if e == 0:
			return(line)
		if e == 1:
			return(eval(line))

def r(x): #converts degrees to radians
	return(float(x) * np.pi/180)

def d(x): #converts radians to degrees
	return(float(x) * 180/np.pi)

def klat(x): #converts kilometers to latitude
	return(float(x) / 110.574)

def klon(x, lat): #converts kilometers to longitude. lat must be in DEGREES
	return(float(x) / (111.32 * math.cos(r(lat))))

def dis(lat1, lon1, lat2, lon2): #calculates the distance between 2 points using the Haversine formula
	a = 0.5 - (math.cos(r(lat2 - lat1)))/2 + math.cos(r(lat1)) * math.cos(r(lat2)) * (1 - math.cos(r(lon2 - lon1))) / 2
	return(12742 * math.asin(a**0.5))

def station_dict(): #makes a dictionary with the locations of all the sites
	sd = {}
	sta_file = open("/home/hippo/bin/movie/site_lat_lon_ele.txt", "r")
	for line in sta_file:
		l = line.split()
		sd[l[0]] = [float(l[1]), float(l[2]), float(l[3]) ]
	return(sd)	

def max_slip(infile, minline, maxline): #makes a color pallet and saves it in CPT.cpt
	print("checking between line {} and {}".format(minline, maxline))
	maxes = []
	for l in range(1, maxline): #substitute (1, size) for numbers to do the whole thing
		slps = []
		d = reader(infile, l, 1)
		if len(d) > 0:
			r = eval(d['result'])
			slp = r['slip']
			for s in slp:
				slps.append(float(s))
			maxes.append(max(slps))
	return(max(maxes))	

def gen_tmq(infile, minline, maxline): #gets times, magnitudes and qualities from an earthquake file
	t0 = eval(reader(infile, 1, 1)['result'])['time']
	off = t0 #+ toffs['Mentawai2010'] # this can be used to correct the times appropriately
	tmqs = []
	for i in range(minline, maxline):
		l = reader(infile, i, 1)
		r = eval(l['result'])
		t = datetime.datetime.fromtimestamp(r['time'] - off).strftime('%Y-%m-%d %H:%M:%S')
		tmqs.append([t, r['Mw'], float("{0:.2f}".format(r['Q']))])
	return(tmqs)

#labeler(5, 7.6, "", "", 1, "/home/hippo/bin/movie/frames1")