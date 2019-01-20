import os
import sys

DIR_TASK = os.path.basename(os.getcwd())
DIR_LIB = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
DIR_TASK = os.path.dirname(os.path.abspath(__file__))

import json, csv, time, string, itertools, copy, yaml
import numpy as np
import pandas as pd
import datetime as dt

CONFIG_FILE_NAME = '005-R1_config'
config = yaml.load( stream = file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'r'))
#yaml.dump( config, file( DIR_TASK + '\\config.yml', 'w') )

sys.path.append( DIR_LIB )

from lib.router import Router
router = Router( )

# --------------------------------------------------------------------------
today = dt.datetime.now().strftime("%Y-%m-%d--%H-%M") 

#STEP: output-file
#com: create output folder
outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )


#STEP: modify version?
configVersion = config['version']
config['version'] =  round( float(configVersion) + .1, 1 ) if config['options']['increment-version'] == True else configVersion


#STEP: load Master-file CSV
sourcePathFile = router.getRoute( config['source']['route'] ) + config['source']['dir'] + config['source']['file']
songs_df = pd.read_csv( filepath_or_buffer=sourcePathFile , sep=";", quoting= 3 )


#TASK: Get the list of top artists
TASK_NAME = 'top-ten-artists'
outputFilePath = outputPath + config['target']['file'].replace("$TASK$", TASK_NAME )
topTen_df = songs_df.sort_values(by=['deezer-quote'], ascending=False).head(10)
topTen_df.to_json(outputFilePath, orient='split')

#TASK: Get the list of top german artists
TASK_NAME = 'top-ten-artists-de'
outputFilePath = outputPath + config['target']['file'].replace("$TASK$", TASK_NAME )
topTenDe_df = songs_df[ songs_df['lang'] == 'de' ].sort_values(by=['deezer-quote'], ascending=False).head(10)
topTenDe_df.to_json(outputFilePath, orient='split')



#STEP: update config file
# yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
