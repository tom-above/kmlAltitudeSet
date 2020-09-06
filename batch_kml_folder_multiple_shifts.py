# -*- coding: utf-8 -*-
"""
Take a folder full of KML files and apply an array of shifts to each {X,Y,Z} and save out to subfolder.
"""
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os
import subprocess
import glob

outpath = '\\offset'
x = 0
z = 33 # meters elevation ABOVE WAYPOINT 1
speed = 4.5 # meters per second
heading = 0 #degrees clockwise from North (0)
parameters = [
#    (x, 0, z, '_0-aligned'), # (x, y, z, _suffix)
#    (x, -0.000036, z, '_4m-S'),
#    (x, 0.000036, z, '_4m-N'),
    # (-0.000003, -0.000009, z, '_1m-S'),
    # (0.000003, 0.000009, z, '_1m-N'),
    (x, -0.000018, z, '_2m-S'),
    (x, 0.000018, z, '_2m-N')
]

# Select an origin folder
Tk().withdraw() # We don't want a full GUI, so keep the root window from appearing
surveyFolderPath = askdirectory(mustexist=True)
surveyFolderPath = os.path.normpath(surveyFolderPath)

kmlFileList = glob.glob(surveyFolderPath + '/*.kml')
for kml in kmlFileList:

    pyCall = 'py C:\\code\\kmlAltitudeSet\\kml_zero_first_elevation.py'

    for pp in parameters:
        osCall = f'{pyCall} -p "{kml}" -x {pp[0]:f} -y {pp[1]:f} -z {pp[2]:f} -s {pp[3]} -sp {speed} -hd {heading} -o {outpath}'
        print(osCall)
        response = subprocess.run(osCall, stderr=subprocess.PIPE)
        returncode = response.returncode
        if returncode > 0:
            print('DANGEROUS ELEVATION DETECTED!')
            exit(1)