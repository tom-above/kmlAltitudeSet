import os
import argparse
from lxml import etree
from pykml import parser

argparser = argparse.ArgumentParser(description='Offset KML')
argparser.add_argument('-p','--path', type=str, help='path to KML file')
argparser.add_argument('-x','--offx', type=float, help='degrees (+East)')
argparser.add_argument('-y', '--offy', type=float, help='degrees (+North)')
argparser.add_argument('-z', '--offz', type=float, help='meters (Zeros to takeoff, so this is offset above takeoff location)')
argparser.add_argument('-s', '--suffix', type=str, help='suffix to add to KML name')
args = argparser.parse_args()
print(args)

def start(filePath,offx,offy,offz,suffix):
    with open(filePath) as fh:
        kml = parser.parse(fh)
    docRoot = kml.getroot()
    #set above ground
    #docRoot.Document.Folder.Placemark.LineString.altitudeMode = 'relativeToGround'
    #get coordinate list
    try:
        oldCoordinates = docRoot.Document.Folder.Placemark.LineString.coordinates
    except:
        oldCoordinates = docRoot.Document.Placemark.LineString.coordinates
    inList = str(oldCoordinates).split(' ')
    
    takeoff = inList[0].split(',')
    takeoffElevation = float(takeoff[2])
    
    outList = []
    for ii in inList:
        waypoint = ii.split(',')
        print(waypoint)
        try:
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
        except:
            print('bad row ignored')

    newCoordinates = ' '.join(outList)
    try:
        docRoot.Document.Folder.Placemark.LineString.coordinates = newCoordinates
    except:
        docRoot.Document.Placemark.LineString.coordinates = newCoordinates

    fileStem = os.path.splitext(filePath)
    fileOut = fileStem[0] + suffix + '.kml'
    docRoot.Document.name = os.path.split(fileOut)[-1]

    stringOut = etree.tostring(docRoot, pretty_print=True).decode('utf-8')

    with open(fileOut, 'w') as fhout:
        fhout.write(stringOut)
        

if os.path.exists(args.path) and os.path.isfile(args.path):
        _, extension = os.path.splitext(args.path)
        if extension == '.kml':
            start(args.path, args.offx, args.offy, args.offz, args.suffix)
            exit(0)
        else:
            print("ERROR: Specified file not a KML file (.kml)")
            exit(1)
else:
    print("ERROR: Couldn't find specified KML file")
    exit(1)