import os
import sys

DIR_TASK = os.path.basename(os.getcwd())
DIR_LIB = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
DIR_TASK = os.path.dirname(os.path.abspath(__file__))

import json, csv, time, string, itertools, copy, yaml
import numpy as np
import pandas as pd
import datetime as dt

from os import listdir
from os.path import isfile, join
import requests

CONFIG_FILE_NAME = '006-R0_config'
config = yaml.load( stream = file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'r'))
#yaml.dump( config, file( DIR_TASK + '\\config.yml', 'w') )

sys.path.append( DIR_LIB )

from lib.router import Router
router = Router( )

# --------------------------------------------------------------------------
today = dt.datetime.now().strftime("%Y-%m-%d--%H-%M") 

#STEP: modify version?

configVersion = config['version']
config['version'] =  round( float(configVersion) + .1, 1 ) if config['options']['increment-version'] == True else configVersion


#STEP: load file json

sourcePathFile = router.getRoute( config['secret']['route'] ) + config['secret']['dir'] + config['secret']['file']
rawObj = open( sourcePathFile , 'r')
secretFile = json.load( rawObj )

sourcePath = router.getRoute( config['source']['route'] ) + config['source']['dir']
sourceFilesNames = [f for f in listdir( sourcePath ) if isfile(join(sourcePath , f))]
# sourceFilesNames.remove('links.json')

#STEP: 

def getGenderByName( _name ):
    # https://genderapi.io/api/?name=Abdullah
    apiUrl = "https://genderapi.io/api/"
    params = {
        "name": _name
    }
    result = requests.get(apiUrl, params=params).json()
    return result["gender"]


participantsData = []

for fileIdx, sourceFileName in enumerate( sourceFilesNames ):
    sourcePathFile = router.getRoute( config['source']['route'] ) + config['source']['dir'] + sourceFilesNames[ fileIdx ]
    rawObj = open( sourcePathFile , 'r')
    fileJsonContent = json.load( rawObj )
    
    participantItem = {
        'name': fileJsonContent['name'],
        'age': fileJsonContent['age'],
        'buzzer_count': fileJsonContent['buzzer_count'],
        'buzzer_coaches': fileJsonContent['buzzer_coaches'],
        'gender': getGenderByName( fileJsonContent['name'].split(" ")[0] )
    }
    participantsData.append( participantItem )


#STEP: output-file

outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir']
outputFilePath = outputPath + config['target']['file'].replace("$VERSION$", str( config['version'] ) )

#com: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )


with open( outputFilePath , 'w') as outfile:
    json.dump( participantsData , outfile , indent=2)

#STEP: update config file

yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
