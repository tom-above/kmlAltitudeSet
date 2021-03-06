import glob
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

suffix = '_0-aligned_3Dpath'

# Select an origin folder
Tk().withdraw() # We don't want a full GUI, so keep the root window from appearing
surveyFolderPath = askdirectory(mustexist=True)
surveyFolderPath = os.path.normpath(surveyFolderPath)

os.chdir(surveyFolderPath)
kmls = glob.glob('*.kml')
for kk in kmls:
    fstem = os.path.splitext(kk)[0]
    print(fstem[(-len(suffix)):])
    if fstem[(-len(suffix)):] == suffix:
        newname = fstem[:(-len(suffix))] + '.kml'
        print(newname)
        os.rename(kk, newname)