import os
import sys

DIR_TASK = os.path.basename(os.getcwd())
DIR_LIB = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
DIR_TASK = os.path.dirname(os.path.abspath(__file__))

import json, csv, time, string, itertools, copy, yaml
import numpy as np
import pandas as pd
import datetime as dt

CONFIG_FILE_NAME = '005-R0_config'
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


#TASK: Get the lang quote % 

TASK_NAME = 'lang-quote'
outputFilePath = outputPath + config['target']['file'].replace("$TASK$", TASK_NAME )

langSongsData = []
languageKeys =  songs_df["lang"].unique()
for langKey in languageKeys:

  langLenSong = len( songs_df[ songs_df["lang"] == langKey ] )
  langItem = {
    'lang_key': langKey,
    'num_songs': int( langLenSong ),
    'total_songs': len( songs_df ),
    'lang_quote' : round( float( langLenSong * 100 / float(len( songs_df )) ) , 2)
  }
  langSongsData.append( langItem )

with open( outputFilePath, 'w') as outfile:
  json.dump( langSongsData , outfile , indent=2)



#STEP: update config file
# yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
