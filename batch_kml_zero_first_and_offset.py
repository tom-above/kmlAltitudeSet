# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 19:00:19 2019

@author: TomHall
"""

import csv
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os
import glob
from scrapeMBJpdf import scrape

Tk().withdraw()
folderin = askdirectory()
os.chdir(folderin)

fileout = 'multipleMBJpDFs.csv'

csvout = open(fileout, 'w', newline='')
fieldnames= [
        'SerialNo',
        'Manufacturer',
        'Model',
        'Class_ABCD',
        'JobID',
        'PMPP_Watt',
        'P_nominal_Watt',
        'Mismatch_perc',
        'LowLightTestIrradiance_WperM2',
        'LowLightPerformance_Watt',
        'CellsNoJudgement_count',
        'CellsJudged_VeryCritical_count',
        'CellsJudged_Critical_count',
        'CellsJudged_Uncritical_count',
        'CellsJudged_OtherELabnormalities_count',
        'TotalCells_count',
        'JudgementComment',
        'ModuleComment',
        'Location_RowNo_int',
        'Location_StringLabel_str',
        'Location_ModuleNumber_int'
]

writer = csv.DictWriter(csvout, fieldnames=fieldnames)
writer.writeheader()

pathStr = folderin+'/*.pdf'
pdfList = glob.glob(pathStr)

for idx, path2PDF in enumerate(pdfList):
    print((idx+1), path2PDF, end=' ')
    rowData = scrape(path2PDF)
    writer.writerow(rowData)
    if rowData['TotalCells_count'] != 60:
        print('!!WARNING: Something other than 60 cells reported!!')
    else:
        print('DONE!')

csvout.close()