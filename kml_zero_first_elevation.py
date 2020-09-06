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
argparser.add_argument('-sp', '--speed', type=str, help='speed in m/s')
argparser.add_argument('-hd', '--heading', type=str, help='heading clockwise from North (0 degrees)')
argparser.add_argument('-o', '--outpath', type=str, nargs='?', const='', help='output path (relative to input path). default = inpath')
args = argparser.parse_args()
print(args)

def start(filePath,offx,offy,offz,suffix,speed,heading,outpath):
    with open(filePath) as fh:
        kml = parser.parse(fh)
    docRoot = kml.getroot()
    #set above ground
    #docRoot.Document.Folder.Placemark.LineString.altitudeMode = 'relativeToGround'
    #get coordinate list
    try:
        oldCoordinates = docRoot.Document.Folder.Placemark.LineString.coordinates
    except:
        try:
            oldCoordinates = docRoot.Document.Placemark.LineString.coordinates
        except:
            for pm in docRoot.Document.Placemark:
                if pm.name == '3D Path':
                    oldCoordinates = pm.LineString.coordinates
                else:
                    docRoot.Document.remove(pm)

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

        if newElevation < 4:
            print('DANGER!! Absolute elevation relative to takeoff < 4m. Exiting for safety.')
            exit(1)

    newCoordinates = ' '.join(outList)
    try:
        docRoot.Document.Folder.Placemark.LineString.coordinates = newCoordinates
    except:
        docRoot.Document.Placemark.LineString.coordinates = newCoordinates

    docRoot.Document.speed=speed
    docRoot.Document.heading=heading

    stringOut = etree.tostring(docRoot, pretty_print=True).decode('utf-8')

    splitPath = os.path.split(filePath)
    pathStem = splitPath[0]
    fileNameStem = os.path.splitext(splitPath[1])[0]
    outStem = f'{pathStem}{outpath}'
    #fileOut = splitPath[0] + '\\' + suffix + '.kml'
    fileOut = f'{outStem}\\{fileNameStem}{suffix}.kml'
    if not os.path.exists(outStem):
        os.mkdir(outStem)

    docRoot.Document.name = os.path.split(fileOut)[-1]

    with open(fileOut, 'w') as fhout:
        fhout.write(stringOut)

if os.path.exists(args.path) and os.path.isfile(args.path):
        _, extension = os.path.splitext(args.path)
        if extension == '.kml':
            start(args.path, args.offx, args.offy, args.offz, args.suffix, args.speed, args.heading, args.outpath)
            exit(0)
        else:
            print("ERROR: Specified file not a KML file (.kml)")
            exit(1)
else:
    print("ERROR: Couldn't find specified KML file")
    exit(1)