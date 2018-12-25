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

CONFIG_FILE_NAME = '002.00_config'
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

#STEP: load
sourcePath = router.getRoute( config['source']['route'] ) + config['source']['dir']
sourceFilesNames = [f for f in listdir( sourcePath ) if isfile(join(sourcePath , f))]
sourceFilesNames.remove('links.json')

'''
Create data frame with: participantName, date, clicks, in, time, dayWeek
- replace characters
-> list by particpant with: {in, clicks, date, time}, sort by date
'''


# STEP: create registry of participants
fileIdx = 0
rawObj = open( sourcePath + sourceFilesNames[ fileIdx ] , 'r')
fileJsonContent = json.load( rawObj )

participantsRegistry = {}

coachNames = ['Michael Patrick', 'Mark', 'Michi & Smudo', 'Yvonne' ]

for coachName in coachNames:
    coachListParticipants = fileJsonContent[ coachName ]
    for coachParticipants in coachListParticipants:
        participantsRegistry[ coachParticipants["name"] ] = {}


# STEP: charge clicks,date,in state for each day captured for each participant
#COM: put content in list "participantsRegistry"
#COM: loop all the files
for fileName in sourceFilesNames:
    #print( fileName )
    try:
        rawObj = open( sourcePath + fileName, 'r')
        fileJsonContent = json.load( rawObj )
        #COM: empty file?
        if len( fileJsonContent ) > 0:
            #COM: fileName = # teams_2018-11-20--00-37.json
            fileDate = fileName.split("_")[1].split("--")[0]
            fileTime = fileName.split("_")[1].split("--")[1].replace(".json","").replace("-",":")
            for coachName in coachNames:
                coachListParticipants = fileJsonContent[ coachName ]
                for coachParticipant in coachListParticipants:
                    if fileDate not in participantsRegistry[ coachParticipant["name"] ]:
                        participantsRegistry[ coachParticipant["name"] ][ fileDate  ] = []
                    item = {
                        "time": fileTime,
                        "likes": coachParticipant["likes"],
                        "in": coachParticipant["in"],
                        "coach": coachName,
                        "date": fileDate
                    }
                    participantsRegistry[ coachParticipant["name"] ][ fileDate  ].append( item )

    except ValueError:
        print 'error open' +  fileName



#STEP: output-file
#COM: Absolute Path
outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir']
outputFilePath = outputPath + config['target']['file'].replace("$VERSION$", str( config['version'] ) )

#COM: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )

#COM: create output file
with open( outputFilePath, 'w') as outfile:
    json.dump( participantsRegistry , outfile , indent=2)


#STEP: update config file
yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
