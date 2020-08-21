# -*- coding: utf-8 -*-
"""
Take a KML file and apply an array of shifts {X,Y,Z} and save out
"""
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import subprocess

# Select an origin KML file
Tk().withdraw()
kmlIn = askopenfilename()

parameters = [
    (0, -0.000036, 23, '_4m-S'), # (x, y, z, _suffix)
    (0, -0.000018, 23, '_2m-S'),
    (0, 0.000018, 23, '_2m-N'),
    (0, 0.000036, 23, '_4m-N')
]

pyCall = 'py C:\\code\\kmlAltitudeSet\\kml_zero_first_elevation.py'

for pp in parameters:
    osCall = f"{pyCall} -p {kmlIn} -x {pp[0]:f} -y {pp[1]:f} -z {pp[2]:f} -s {pp[3]}"
    print(osCall)
    subprocess.call(osCall)