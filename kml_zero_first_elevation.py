import os
import argparse
from lxml import etree
from pykml import parser
import utm

argparser = argparse.ArgumentParser(description='Offset KML')
argparser.add_argument('path', help='path to KML file')
argparser.add_argument('offE', help='meters (+East)')
argparser.add_argument('offN', help='meters (+North)')
argparser.add_argument('offZ', help='meters (Zeros to takeoff, so this is offset above takeoff location)')
args = argparser.parse_args()

def calculate_new_location_from_offset_meters(longIn, latIn, offE, offN):

    #convert to UTM (meters) and get relevant zone
    utmIn = utm.from_latlon(latIn, longIn)
    eastingsIn = utmIn[0]
    northingsIn = utmIn[1]
    UTMzoneNumber = utmIn[2]
    UTMzoneLetter = utmIn[3]
    #add offsets (can be negative for W/S)
    eastingsOut = eastingsIn + offE
    northingsOut = northingsIn + offN

    #convert new coordinates back to lat-long
    latlongOut = utm.to_latlon(eastingsOut, northingsOut, UTMzoneNumber, UTMzoneLetter)

    #utm module returns latitude first
    latOut = latlongOut[0]
    longOut = latlongOut[1]

    #this function returns longitude first because that is 'x'
    return longOut, latOut

def start(filePath,offE,offN,offZ):
    with open(filePath) as fh:
        kml = parser.parse(fh)
    docRoot = kml.getroot()
    #set above ground
    #docRoot.Document.Folder.Placemark.LineString.altitudeMode = 'relativeToGround'
    #get coordinate list
    try: #usual for Agisoft KMLs
        oldCoordinates = docRoot.Document.Folder.Placemark.LineString.coordinates
        KMLformat = 'agisoft'
    except AttributeError:
        try: #usual for Google Earth KMLs
            oldCoordinates = docRoot.Document.Placemark.LineString.coordinates
            KMLformat = 'google-earth'
        except AttributeError as e:
            print('ERROR! KML format not recognised: {0}'.format(e))
            exit(1)

    inList = str(oldCoordinates).split(' ')
    
    takeoff = inList[0].split(',')
    takeoffElevation = float(takeoff[2])
    
    outList = []
    for ii in inList:
        waypoint = ii.split(',')
        print(waypoint)

        try:
            float(waypoint[0])
            success = True
        except:
            print('not a valid coordinate')
            success = False

        if success:

            longIn = float(waypoint[0])
            latIn = float(waypoint[1])

            #convert to UTM to add meters then convert back to spherical
            #this function takes longitude (x) first then latitude (yp)
            longOut, latOut = calculate_new_location_from_offset_meters(longIn, latIn, offE, offN)

            #long
            waypoint[0] = str(longOut)
            #lat
            waypoint[1] = str(latOut)
            #elevation
            oldElevation = float(waypoint[2])
            newElevation = oldElevation - takeoffElevation + offZ
            waypoint[2] = str(newElevation)
            print(waypoint)

            wayPointString = ','.join(waypoint)
            outList.append(wayPointString)
    
    newCoordinates = ' '.join(outList)
    if KMLformat == 'agisoft':
        docRoot.Document.Folder.Placemark.LineString.coordinates = newCoordinates
    elif KMLformat == 'google-earth':
        docRoot.Document.Placemark.LineString.coordinates = newCoordinates
    else:
        print('ERROR: KML format invalid')
        exit(1)

    stringOut = etree.tostring(docRoot, pretty_print=True).decode('utf-8')

    fileStem = os.path.splitext(filePath)
    fileOut = fileStem[0] + '_zeroed' + '.kml'

    with open(fileOut, 'w') as fhout:
        fhout.write(stringOut)
        

if os.path.exists(args.path) and os.path.isfile(args.path):
    _, extension = os.path.splitext(args.path)
    if extension == '.kml':
        start(args.path,float(args.offE),float(args.offN),float(args.offZ))
        exit(0)
    else:
        print("ERROR: Specified file not a KML file (.kml)")
        exit(1)
else:
    print("ERROR: Couldn't find specified KML file")
    exit(1)