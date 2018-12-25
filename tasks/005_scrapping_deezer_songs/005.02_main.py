# -*- coding: utf-8 -*-
import os
import sys

DIR_TASK = os.path.basename(os.getcwd())
DIR_LIB = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
DIR_TASK = os.path.dirname(os.path.abspath(__file__))

import json, csv, time, string, itertools, copy, yaml
import numpy as np
import pandas as pd
import datetime as dt

from langdetect import detect
import langid
langid.set_languages( ['es','en','de','it','fr'] )
from guess_language import guess_language


CONFIG_FILE_NAME = '005.02_config'
config = yaml.load( stream = file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'r'))
#yaml.dump( config, file( DIR_TASK + '\\config.yml', 'w') )

sys.path.append( DIR_LIB )

from lib.router import Router
router = Router( )

# --------------------------------------------------------------------------

#STEP: modify version?

configVersion = config['version']
config['version'] =  round( float(configVersion) + .1, 1 ) if config['options']['increment-version'] == True else configVersion


sourcePathFile = router.getRoute( config['source']['route'] ) + config['source']['dir'] + config['source']['file']
dezzerSongs_df =pd.read_csv( filepath_or_buffer = sourcePathFile , sep=";", quoting= 3, skip_blank_lines=True )

def removeText( row ):
  return row["song"].split('(')[0].replace('"','').strip()

dezzerSongs_df['song'] = dezzerSongs_df.apply( removeText, axis=1)


def detectSongLanguage( row ):
  # detect( row["song"] ),
  # langid.classify(row["song"])[0]
  # print( row["song"], langid.classify(row["song"])[0] ) 
  return langid.classify(row["song"])[0]

dezzerSongs_df['lang'] = dezzerSongs_df.apply( detectSongLanguage, axis=1)

#print dezzerSongs_df[ ["lang","song"] ]


#STEP: output-file

outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 
outputFilePath = outputPath + config['target']['file'].replace("$VERSION$", str( config['version'] ) )

#com: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )

dezzerSongs_df.to_csv( path_or_buf = outputFilePath , sep=";", quoting=None, index=False )

#STEP: update config file

yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
