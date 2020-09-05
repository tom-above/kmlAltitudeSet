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

x = 0
z = 23 # meters elevation
parameters = [
    (x, 0, z, '_0-aligned'), # (x, y, z, _suffix)
    (x, -0.000036, z, '_4m-S'),
    (x, -0.000018, z, '_2m-S'),
    (x, 0.000018, z, '_2m-N'),
    (x, 0.000036, z, '_4m-N')
]

pyCall = 'py C:\\code\\kmlAltitudeSet\\kml_zero_first_elevation.py'

for pp in parameters:
    osCall = f'{pyCall} -p "{kmlIn}" -x {pp[0]:f} -y {pp[1]:f} -z {pp[2]:f} -s {pp[3]} -o'
    print(osCall)
    subprocess.call(osCall)