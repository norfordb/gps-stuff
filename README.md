# gps-stuff

plotting software for PANGA's rtGNSS inversion software

This software relies on gmt-python. Instructions for installation can be found here:
https://www.gmtpython.xyz/latest/install.html

Begin by downloading an output file from a testing version of the rtGNSS scirpts. Save it as, for example, movie/inputs/Tohoku001.d
Then set:

mod = "Tohoku" 

in run2.py, as launch it with:

python run2.py 001 1   

to save the frames in the move/frames1 directory.


If you encounter errors with matplotlib.pyplot, try 'conda install python.app' and use pythonw rather than python
