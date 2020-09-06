import glob
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

# Select an origin folder
Tk().withdraw() # We don't want a full GUI, so keep the root window from appearing
surveyFolderPath = askdirectory(mustexist=True)
surveyFolderPath = os.path.normpath(surveyFolderPath)

os.chdir(surveyFolderPath)
kmls = glob.glob('*.kml')
print(kmls)
for kk in kmls:
    fstem = os.path.splitext(kk)[0]
    print(fstem)
    print(fstem[-10:])
    if fstem[-10:] == '_0-aligned':
        #print(kk)
        newname = fstem[:-10] + '.kml'
        os.rename(kk, newname)