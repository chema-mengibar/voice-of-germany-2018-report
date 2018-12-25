import os
import sys

from os import listdir
from os.path import isfile, join

DIR_TASK = os.path.basename(os.getcwd())
DIR_LIB = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
DIR_TASK = os.path.dirname(os.path.abspath(__file__))

import json, csv, time, string, itertools, copy, yaml
import numpy as np
import pandas as pd
import datetime as dt

CONFIG_FILE_NAME = '004.00_config'
config = yaml.load( stream = file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'r'))
#yaml.dump( config, file( DIR_TASK + '\\config.yml', 'w') )

sys.path.append( DIR_LIB )

from lib.router import Router
router = Router( )
print '>> Walk, Don`t Run'
# --------------------------------------------------------------------------
#STEP: modify version?

configVersion = config['version']
config['version'] =  round( float(configVersion) + .1, 1 ) if config['options']['increment-version'] == True else configVersion

halfFinalDate = config['params']['half-final_date']
d = dt.datetime.strptime( halfFinalDate , '%d.%m.%Y')
filePrefix = 'teams_' + d.strftime('%Y-%m-%d')

#STEP: load web-likes from half-final day
sourcePath = router.getRoute( config['source']['web-teams']['route'] ) + config['source']['web-teams']['dir']
sourceFilesNames = [f for f in listdir( sourcePath ) if filePrefix in f ]
sourceFilesNames.sort()

coachNames = ['Michael Patrick', 'Mark', 'Michi & Smudo', 'Yvonne' ]

def getTimeDataStart( _fileIndex ):
    #INFO: global list of sourceFilesNames
    #COM: get list of current active participants
    fileName = sourceFilesNames[ _fileIndex ]
    rawObj = open( sourcePath + fileName, 'r')
    fileJsonContent = json.load( rawObj )

    timeData = {}
    #COM: empty file?
    if len( fileJsonContent ) > 0:
        fileTime = fileName.split("_")[1].split("--")[1].replace(".json","").replace("-",":")
        for coachName in coachNames:
            coachListParticipants =  list(filter(lambda item: item['in'] == True, fileJsonContent[ coachName ] ))
            timeData[ coachName ] = {
                'participants': [ { 'name': f['name'], 'likes':f['likes'] } for f in coachListParticipants ],
                'time': fileTime
            }
    return timeData

def getTimeDataEnd( _fileIndex, _startData ):
    #INFO: global list of sourceFilesNames
    #COM: get list of participants present in the param list
    fileName = sourceFilesNames[ _fileIndex ]
    rawObj = open( sourcePath + fileName, 'r')
    fileJsonContent = json.load( rawObj )

    #COM: flag List of start participants
    startParticipants = []
    for coach in _startData:
        startParticipants.extend( list( map( lambda participant: participant['name'] , [ p for p in _startData[coach]['participants'] ] ) ) )

    timeData = {}
    #COM: empty file?
    if len( fileJsonContent ) > 0:
        fileTime = fileName.split("_")[1].split("--")[1].replace(".json","").replace("-",":")
        for coachName in coachNames:
            coachListParticipants =  list(filter(lambda item: item['name'] in startParticipants, fileJsonContent[ coachName ] ))
            timeData[ coachName ] = {
                'participants': [ { 'name': f['name'], 'likes':f['likes'] } for f in coachListParticipants ],
                'time': fileTime
            }
    return timeData


timeData_start = getTimeDataStart( 0 )
timeData_end = getTimeDataEnd( -1, timeData_start )

hfData = {
    'start': timeData_start,
    'end': timeData_end,
}

#STEP: output-file
#COM: Absolute Path
outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir']
outputFilePath = outputPath + config['target']['file'].replace("$VERSION$", str( config['version'] ) )

#COM: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )

#COM: create output file
with open( outputFilePath, 'w') as outfile:
    json.dump( hfData , outfile , indent=2)