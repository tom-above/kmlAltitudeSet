import os
import argparse
import subprocess
from lxml import etree
from pykml import parser

argparser = argparse.ArgumentParser(description='Offset KML')
argparser.add_argument('path', help='Path to folder that needs processing. Will process all subfolders.')
argparser.add_argument('offx', help='degrees (+East)')
argparser.add_argument('offy', help='degrees (+North)')
argparser.add_argument('offz', help='meters (Zeros to takeoff, so this is offset above takeoff location)')
args = argparser.parse_args()

def start_file(filePath,offx,offy,offz):
    with open(filePath) as fh:
        kml = parser.parse(fh)
    docRoot = kml.getroot()
    #set above ground
    #docRoot.Document.Folder.Placemark.LineString.altitudeMode = 'relativeToGround'
    #get coordinate list
    oldCoordinates = docRoot.Document.Folder.Placemark.LineString.coordinates
    inList = str(oldCoordinates).split(' ')
    
    takeoff = inList[0].split(',')
    takeoffElevation = float(takeoff[2])
    
    outList = []
    for ii in inList:
        waypoint = ii.split(',')
        print(waypoint)
        #long
        oldX = float(waypoint[0])
        newX = oldX + offx
        waypoint[0] = str(newX)
        #lat
        oldY = float(waypoint[1])
        newY = oldY + offy
        waypoint[1] = str(newY)        
        #elevation
        oldElevation = float(waypoint[2])
        newElevation = oldElevation - takeoffElevation + offz
        waypoint[2] = str(newElevation)
        print(waypoint)

        wayPointString = ','.join(waypoint)
        outList.append(wayPointString)
    
    newCoordinates = ' '.join(outList)
    docRoot.Document.Folder.Placemark.LineString.coordinates = newCoordinates
    stringOut = etree.tostring(docRoot, pretty_print=True).decode('utf-8')

    fileStem = os.path.splitext(filePath)
    fileOut = fileStem[0] + '_zeroed' + '.kml'

    with open(fileOut, 'w') as fhout:
        fhout.write(stringOut)

def start_dir(dirPath,offx,offy,offz):
    subdirectories = [x[0] for x in os.walk(dirPath)]

    for d in subdirectories:
        os.chdir(d)
        allFiles = os.listdir(os.getcwd())
        for f in allFiles:
            _, extension = os.path.splitext(f)
            if extension == '.kml':
                start_file(f,offx,offy,offz)
            else:
                print('{} is not a KML file'.format(f))

###        

if os.path.exists(args.path) and os.path.isdir(args.path):
    start_dir(args.path,float(args.offx),float(args.offy),float(args.offz))
    exit(0)
else:
    print("Path is not a directory")
    exit(1)