#import gmt
import numpy as np
import matplotlib
import multiprocessing as mp
from functools import partial
import linecache as lc

def reader(fi, li, e): #opens the input files. 0 as 3rd argument gets you the line as it is, 1 returns eval(line), to convert script outputs to dictionaries
	line = lc.getline(fi, li)
	if line is None:
		pass
	else:
		if e == 0:
			return(line)
		if e == 1:
			return(eval(line))

def plot(corners, lats, lons, mdxs, mdys, edxs, edys, slips, maxslip, reg, proj, outfile, scale, imdir, scalelat, scalelon): #this function generates the frames
	import gmt
	testcors = [[corners[0][0][0], corners[0][0][1]], [corners[0][1][0], corners[0][1][1]], [corners[0][2][0], corners[0][2][1]], [corners[0][3][0], corners[0][3][1]]]
	fig = gmt.Figure()
	fig.basemap(R=reg, J=proj, frame=True)
	#fig.grdimage("land-water_0.5m.grd", cmap="geo", C="land-water11.cpt", I="land-water_0.5m.grad", t=0) #for pretty topography from the indicated cpt file
	#fig.coast(R=reg, J=proj, frame=True, N="a/1p", W="1p", D="i") #plots the borders (a = all political boundaries, W gets coastline)
	fig.coast(R=reg, J=proj, G='darkgray', S="white", B=True) #plots the land, G colors the land, S colors the water
	for i in range(int(len(corners))): #plots the polygons
		fig.plot(list(zip(*corners[i]))[0], list(zip(*corners[i]))[1], L=True, G=hxc(slips[i], maxslip), t=50, W='0.5p,black', pen='0.5p,black')	
	num = outfile.split("_")[-1][:-4]
	fig.grdimage("{}/lab{}.png".format(imdir,num), J="X1.5i") #puts the labels on
	fig.plot(lons, lats, style='c0.1c', color='red', J=proj, W='1p,black') #plots points for GPS stations
	fig.plot(x=lons, y=lats, direction=[mdxs, mdys], style='V0.2c+e+n+z{}c'.format(scale), color='blue', pen='0.30p,blue', t=30) #plots the measured vectors
	fig.plot(x=lons, y=lats, direction=[edxs, edys], style='V0.2c+e+n+z{}c'.format(scale), color='red', pen='0.30p,red', t=30) #plots the estimated vectors	
	fig.plot(x=[scalelon,0], y=[scalelat,0], direction=[[0,0], [0.5,0.5]], style='V0.5c+e+n+z{}c'.format(scale), color='black', pen='1.5p,black') #plots a scale vector - set to 0.5 meters!!!
	fig.savefig(outfile, show=False) #saves the figure and doesn't show it

def poly_read(fi): #reads a polygon file and returns a list of list that can be plotted
	ncors = []
	i = 0
	with open("{}".format(fi), "r") as f:
		ncor = []
		lats = []
		lons = []
		for line in f:
			ls = line.split(" ")
			ncor.append([float(ls[0]), float(ls[1]), np.abs(float(ls[2]))])
			lat = [float(ls[0])]
			lon = [float(ls[1])]
			if i % 4 == 3:
				lat.append(float(ls[0]))
				lon.append(float(ls[1]))				
				ncors.append(ncor)
				ncor = []
				lat = []
				lon = []
			i += 1
	return(ncors)

def plot_prep(indat, sd, polydir="/home/hippo/bin/movie/polygons/"): #pulls out the data that we'll be plotting
	mod = indat['model'] #lets the software plot the model given in the data
	res = eval(indat['result'])
	dat = res['data']
	est = res['estimates']
	slp = res['slip']
	t = int(res['time'])
	q = float(res['Q'])
	lab = res['label']
	lats = []
	lons = []
	ddla = []
	ddlo = []
	edla = []
	edlo = []
	for d in dat:
		lats.append(sd[d[0]][0])
		lons.append(sd[d[0]][1])
		ddla.append(float(d[2]))
		ddlo.append(float(d[1]))
	for e in est:
		edla.append(float(e[2]))
		edlo.append(float(e[1]))
	cors = poly_read("{}{}.polygon".format(polydir, mod))
	return(cors, lats, lons, ddla, ddlo, edla, edlo, mod, q, lab, slp)
	
def hxc(cval, maxslip): #for the colormap
	cmap = matplotlib.cm.get_cmap('jet')
	rgba = cmap(float(cval)/float(maxslip))
	return(matplotlib.colors.rgb2hex(rgba))

def plot_fun(f, i, sd, mslip, reg, proj, scale, fmt, imdir, scalelat, scalelon):
	print("Plotting timestep", i)
	inf = reader(f, i, 1)
	cors, lats, lons, ddla, ddlo, edla, edlo, mod, q, lab, slp = plot_prep(inf, sd)
	plot(cors, lats, lons, ddlo, ddla, edlo, edla, slp, mslip, reg, proj, "{}/mov-test_{}.{}".format(imdir, i, fmt), scale, imdir, scalelat, scalelon) #png - use this for movies	

def caller(f, sd, maxslip, reg, proj, scale, framedir, scalelat, scalelon, i):
	plot_fun(f, i, sd, maxslip, reg, proj, scale, "png", framedir, scalelat, scalelon)

def multi(f, sd, maxslip, reg, proj, scale, framedir, scalelat, scalelon, minline, maxline):
	call = partial(caller, f, sd, maxslip, reg, proj, scale, framedir, scalelat, scalelon)
	#with mp.Pool(mp.cpu_count()) as p:
	with mp.Pool(4) as p:
		a = p.map(call,[x for x in range(minline, maxline)])	
