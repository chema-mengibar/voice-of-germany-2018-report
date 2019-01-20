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

import math
import re

CONFIG_FILE_NAME = '009.00_config'
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


#STEP: load source files
source = config['source']['source_blinds']
fileIdx = 0
sourcePathFile = router.getRoute( source['route'] ) + source['dir'] + source['files'][fileIdx]
rawFile = open( sourcePathFile , 'r')
blindsFileLinesRaw = [line.rstrip('\n') for line in rawFile]
blindsFileLines = filter(None, blindsFileLinesRaw)

source = config['source']['source_team']
fileIdx = 0
sourcePathFile = router.getRoute( source['route'] ) + source['dir'] + source['files'][fileIdx]
rawFile = open( sourcePathFile , 'r')
coachesTeamsObj = json.load( rawFile )
coachesNames = coachesTeamsObj.keys() # ['Michael Patrick', 'Mark', 'Michi & Smudo', 'Yvonne' ]

source = config['source']['source_buzzers']
fileIdx = 0
sourcePathFile = router.getRoute( source['route'] ) + source['dir'] + source['files'][fileIdx]
rawFile = open( sourcePathFile , 'r')
participantsObj = json.load( rawFile )

source = config['source']['source_deezer']
fileIdx = 0
sourcePathFile = router.getRoute( source['route'] ) + source['dir'] + source['files'][fileIdx]
deezerSongs = pd.read_csv( filepath_or_buffer = sourcePathFile , sep=";", quoting= 3 )

#DEF:
def lineSplitColumns( _dataLine ):
  regResults = re.search('^(\d)-\s*(\d+).\s*(\D+):\s+\"\s*(\D+)\"\D+-\s+(\D+)', _dataLine)
  if regResults is not None:
    r_showId = regResults.group(1)
    r_turn = regResults.group(2)
    r_participant = regResults.group(3)
    r_songTitle = regResults.group(4)
    r_songArtist = regResults.group(5)
    return [ r_showId, r_turn, r_participant, r_songTitle, r_songArtist ]
  return []  


def searchParticipantCoach( _participantName ):
  # globals: coachesTeamsObj, coachesNames
  nameEncoded = _participantName.decode('utf-8')
  for coachName in coachesNames:
    teamList = coachesTeamsObj[ coachName ]
    search = [ itemTeam for itemTeam in teamList  if itemTeam['name'] == nameEncoded ]
    if len(search) > 0:
      return coachName
    

def getParticipantInfo( _participantName ):
  # globals: participantsObj
  nameEncoded = _participantName.decode('utf-8')
  return [ partTeam for partTeam in participantsObj  if partTeam['name'] == nameEncoded ]


def findSongInDeezer( _songTitle ):

  df_testRow = deezerSongs[ deezerSongs['song'].str.lower() == _songTitle.lower() ]
  try:
    df_deezerRow = df_testRow.iloc[0]
    test = df_testRow.iloc[0]['artist']
  except:
    songTitleWords = _songTitle.lower().split(" ")
    regexParts = [ '(?:@' + word + '@)' for word in songTitleWords ]
    strRegex = '|'.join(regexParts)

    deezerSongs['affinity'] = 0

    def regex_filter( _row ):
      #com: create a empty space around each word
      _value = _row['song']
      newValueWidthSpaces = '@' + '@@'.join( _value.lower().split(' ') ) + '@'
      searchResult = re.findall( strRegex, newValueWidthSpaces )  # res = re.search( strRegex, _value)
      _row['affinity'] =  len( searchResult )
      return _row
     
    #df_rowsResultSearch = deezerSongs[ deezerSongs.apply( regex_filter, axis=1 ) ]
    df_testRow = deezerSongs.apply( regex_filter, axis=1 )
    df_deezerRow = df_testRow.iloc[ df_testRow['affinity'].idxmax() ]


  # print ( 0 if math.isnan( float(df_deezerRow['year']) ) else int(df_deezerRow['year']) ),
  return [
    df_deezerRow['artist'] ,
    int(df_deezerRow['year'] ) if str(df_deezerRow['year']).isdigit()  else 0,
    ( 0 if math.isnan( (df_deezerRow['deezer-quote']) ) else float(df_deezerRow['deezer-quote']) ),
    ( '' if str(df_deezerRow['genre']) == 'nan' else str(df_deezerRow['genre']) ),
    df_deezerRow['lang'],
  ]  
      
episodes = 0
languages = []
blindsData = []

# HELP: filter list of lines by text
## test1 = [ part for part in blindsFileLines if 'Julian Coles' in part ]

# print findSongInDeezer( 'Breakfest in America' )
# sys.exit(0)

for idxLine, line in enumerate( blindsFileLines ):

  lineList = lineSplitColumns( line )
  
  participant_name = lineList[2]
  song_title = lineList[3]

  blindsDataObject = { }

  blindsDataObject['participant_main_turn'] = idxLine + 1
  
  blindsDataObject['show_episode'] = int(lineList[0])
  episodes = max( episodes, int(lineList[0]) )
  blindsDataObject['participant_show_turn'] = int(lineList[1])
  blindsDataObject['participant_name'] = participant_name #.encode('utf-8')
    
  coachName = searchParticipantCoach( participant_name )
  blindsDataObject['coach_name'] = coachName if coachName is not None else  ''
  
  participantInfo = getParticipantInfo( participant_name )
  if len( participantInfo ) > 0 :
    blindsDataObject['participant_gender'] = participantInfo[0]['gender']
    #WARN: age format in multiple particpants
    # multi ->  "participant_age": "29, 34 UND 44", 
    # single ->  "participant_age": 28, 
    blindsDataObject['participant_age'] = participantInfo[0]['age']
    blindsDataObject['buzzer_count'] = participantInfo[0]['buzzer_count']
    blindsDataObject['buzzer_coaches_names'] = participantInfo[0]['buzzer_coaches']
  else:
    blindsDataObject['buzzer_count'] = 0
  
  deezerData = findSongInDeezer( song_title )

  blindsDataObject[ 'song_title' ] = song_title
  blindsDataObject['song_artist'] = deezerData[0]
  blindsDataObject['song_year'] = deezerData[1]
  blindsDataObject['song_deezer-quote'] = deezerData[2]
  blindsDataObject['song_genre'] = deezerData[3]
  blindsDataObject['song_lang'] =  deezerData[4]
  
  if( deezerData[4] not in languages ):
    languages.append( deezerData[4] )

  blindsData.append( blindsDataObject )

df_years = deezerSongs['year'].dropna()
df_years = df_years[ df_years.apply(lambda x: x.isdigit())]

# print df_years.max()
# sys.exit(0)

reportData = {
  'auditions_candidates': len( blindsData ),
  'candidates_excluded': len( filter( lambda x: x['buzzer_count'] == 0 , blindsData ) ),
  'candidates_next': len( filter( lambda x: x['buzzer_count'] > 0 , blindsData ) ),
  'candidates_data': blindsData,
  'coaches_keys': coachesNames,
  'languages_keys': languages,
  'auditions_shows' : episodes, 
  'songs_deezer_quotes':{
    'min': float(deezerSongs['deezer-quote'].min()),
    'max':  float(deezerSongs['deezer-quote'].max()),
  },
  'songs_years':{
    'min': int(df_years.min()),
    'max':  int(df_years.max()),
  },

}

#STEP: output-file

outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 
outputFilePath = outputPath + config['target']['file'].replace("$VERSION$", str( config['version'] ) )

#com: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )

with open( outputFilePath , 'w') as outfile:
    json.dump( reportData , outfile , indent=2, ensure_ascii=False)

#STEP: update config file

yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
