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

CONFIG_FILE_NAME = '010.00_config'
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
source = config['source']['source_quotes']
fileIdx = 0
sourcePathFile = router.getRoute( source['route'] ) + source['dir'] + source['files'][fileIdx]
df_showQuotes = pd.read_csv( filepath_or_buffer = sourcePathFile , sep=";", quoting= 3, decimal=',' )

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

def getRawSourceLines( _idx ):
  source = config['source']['source_half-finals']
  fileIdx = _idx
  sourcePathFile = router.getRoute( source['route'] ) + source['dir'] + source['files'][fileIdx]
  rawFile = open( sourcePathFile , 'r')
  fileLinesRaw = [line.rstrip('\n') for line in rawFile]
  return fileLinesRaw
  # fileLines = filter(None, blindsFileLinesRaw)


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
  search = [ partTeam for partTeam in participantsObj  if partTeam['name'] == nameEncoded ]
  return search

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

showLinesExtend = []

#COM: merge lists
showLinesExtend.extend( getRawSourceLines(0) )
showLinesExtend.extend( getRawSourceLines(1) )
showLinesExtend.extend( getRawSourceLines(2) )
showLinesExtend.extend( getRawSourceLines(3) )

#COM: remove empty lines
blackList = [ ' ', '' ]
removeEmptyLines = [ item for item in showLinesExtend if item not in blackList  ]

candidateSongList = []

#COM: join artist and song lines in one
iterator = iter(removeEmptyLines)
for idxLine, line in enumerate( iterator ):
  candidateSongList.append( [line, next(iterator)] )

languages = []
showData = []

for idxCS, candidateSongItem in enumerate( candidateSongList ):
  
  participant_name = candidateSongItem[0]

  song_title = candidateSongItem[1].split(' von ')[0].replace('"','')

  showDataObject = { }
  
  showDataObject['participant_name'] = participant_name #.encode('utf-8')
  showDataObject['coach_name'] = searchParticipantCoach( participant_name )

  df_row = df_showQuotes.loc[ (df_showQuotes['participant'] == participant_name) ]
  quoteObj = {
    'procent': float( df_row['rate_procent'].values[0] ),
    'team': df_row['coach'].values[0],
    'is_winner': True if df_row['coach'].values[0]=='+' else False,
  }
  showDataObject['quotes'] = quoteObj 

  participantInfo = getParticipantInfo( participant_name )
  if len( participantInfo ) > 0 :
    showDataObject['participant_gender'] = participantInfo[0]['gender']
    #WARN: age format in multiple particpants
    # multi ->  "participant_age": "29, 34 UND 44", 
    # single ->  "participant_age": 28, 
    showDataObject['participant_age'] = participantInfo[0]['age']
    showDataObject['buzzer_count'] = participantInfo[0]['buzzer_count']
    showDataObject['buzzer_coaches_names'] = participantInfo[0]['buzzer_coaches']
  else:
    showDataObject['buzzer_count'] = 0

  deezerData = findSongInDeezer( song_title )

  songObject = {}
  songObject[ 'song_title' ] = song_title
  songObject['song_artist'] = deezerData[0]
  songObject['song_year'] = deezerData[1]
  songObject['song_deezer-quote'] = deezerData[2]
  songObject['song_genre'] = deezerData[3]
  songObject['song_lang'] =  deezerData[4]

  showDataObject['songs'] = songObject
  
  if( deezerData[4] not in languages ):
    languages.append( deezerData[4] )

  showData.append( showDataObject )

df_years = deezerSongs['year'].dropna()
df_years = df_years[ df_years.apply(lambda x: x.isdigit())]  

reportData = {
  'auditions_candidates': len( showData ),
  'candidates_data': showData,
  'coaches_keys': coachesNames,
  'languages_keys': languages,
  'show-type':'half-final',
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