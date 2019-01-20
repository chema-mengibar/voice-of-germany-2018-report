import os
import sys

DIR_TASK = os.path.basename(os.getcwd())
DIR_LIB = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
DIR_TASK = os.path.dirname(os.path.abspath(__file__))

import json, csv, time, string, itertools, copy, yaml
import numpy as np
import pandas as pd
import datetime as dt

import re

CONFIG_FILE_NAME = '008.00_config'
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
source = config['source']['source_a']
fileIdx = 0
sourcePathFile = router.getRoute( source['route'] ) + source['dir'] + source['files'][fileIdx]
rawFile = open( sourcePathFile , 'r')
lines = [line.rstrip('\n') for line in rawFile]

linesA = filter(None, lines)
blocks = list(zip(*[iter(linesA)] * 2))

fileName = source['files'][fileIdx]
res = re.search('coach.(.+?)_', fileName)
coachName = res.group(1)
print coachName
sys.exit(0)

#STEP: output-file

outputPath =  router.getRoute( config['target']['route'] ) \
+ config['target']['dir'] \

outputFilePath = outputPath \
+ config['target']['file'].replace("$VERSION$", str( config['version'] ) )

#com: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )




#STEP: update config file

yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
