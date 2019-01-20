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

CONFIG_FILE_NAME = '011.00_config'
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
source = config['source']['source_team']
fileIdx = 0
sourcePathFile = router.getRoute( source['route'] ) + source['dir'] + source['files'][fileIdx]
rawFile = open( sourcePathFile , 'r')
coachesTeamsObj = json.load( rawFile )


#STEP: Buzzers to get candidate data
source = config['source']['source_buzzers']
fileIdx = 0
sourcePathFile = router.getRoute( source['route'] ) + source['dir'] + source['files'][fileIdx]
rawFile = open( sourcePathFile , 'r')
participantsObj = json.load( rawFile )

#DEF:
def getParticipantInfo( _participantName ):
  # globals: participantsObj
  nameEncoded = _participantName.decode('utf-8')
  return [ part for part in participantsObj  if part['name'] == nameEncoded ][0]


#STEP: Get candidates List and Ages
coachesNames = coachesTeamsObj.keys() # ['Michael Patrick', 'Mark', 'Michi & Smudo', 'Yvonne' ]
candidatesNames = []
for coachBlock in coachesTeamsObj:
  candidatesNames.extend( [ item['name'].encode('utf8') for item in coachesTeamsObj[coachBlock] ] )

candidatesData = {}
for name in candidatesNames:
  candidatesData[ name ] = getParticipantInfo( name )

def getCandidateAge( _candidateName ):
  if _candidateName in candidatesData:
    ageStr = candidatesData[ _candidateName ]['age']
    #COM: Clear for -> 29, 34 UND 44
    if str(ageStr).isdigit():
      return int( ageStr )
    else:
      agesItems = ageStr.replace(',','').split(' ')
      ages = [ int(age) for age in agesItems if age.isdigit() ]
      return int( np.mean( ages ) )
  else:
    return 0

candidatesAges = {}
for name in candidatesNames:
  candidatesAges[ name ] = getCandidateAge( name )

CANDIDATES_AGES = candidatesAges


#STEP: Deezer file
source = config['source']['source_deezer']
fileIdx = 0
sourcePathFile = router.getRoute( source['route'] ) + source['dir'] + source['files'][fileIdx]
deezerSongs = pd.read_csv( filepath_or_buffer = sourcePathFile , sep=";", quoting= 3 )


#DEF
#COM: common get-file funtions fot txt files
def getRawSourceLines( _idx, _sourceName ):
  source = config['source'][_sourceName]
  fileIdx = _idx
  sourcePathFile = router.getRoute( source['route'] ) + source['dir'] + source['files'][fileIdx]
  rawFile = open( sourcePathFile , 'r')
  fileLinesRaw = [line.rstrip('\n') for line in rawFile]
  return fileLinesRaw

#COM: song finder in deezer list
def findSongInDeezer( _songTitle ):

  df_testRow = deezerSongs[ deezerSongs['song'].str.lower() == _songTitle.lower() ]
  try:
    df_deezerRow = df_testRow.iloc[0]
    test = df_testRow.iloc[0]['artist']
  except:
    songTitleWords = _songTitle.lower().split(" ")
    regexParts = [ '(?:@' + word + '@)' for word in songTitleWords ]
    strRegex = '|'.join(regexParts).replace('*','\*')

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

  #TEST: print ( 0 if math.isnan( float(df_deezerRow['year']) ) else int(df_deezerRow['year']) ),

  if( df_deezerRow['lang'] not in LANGUAGES ):
    LANGUAGES.append( df_deezerRow['lang'] )
    
  return {
    'artist': df_deezerRow['artist'],
    'title': df_deezerRow['song'], #  _songTitle,
    'year': int(df_deezerRow['year'] ) if str(df_deezerRow['year']).isdigit()  else 0,
    'deezer_quote': ( 0 if math.isnan( (df_deezerRow['deezer-quote']) ) else float(df_deezerRow['deezer-quote']) ),
    'genre': ( '' if str(df_deezerRow['genre']) == 'nan' else str(df_deezerRow['genre']) ),
    'lang': df_deezerRow['lang'],
  } 

#COM: line-parser function to blind-file
def lineSplitColumns( _dataLine ):
  regResults = re.search('^(\d)-\s*(\d+).\s*(\D+):\s+\"\s*(\D+)\"\D*-\s+(\D+)', _dataLine)
  if regResults is not None:
    r_showId = regResults.group(1)
    r_turn = regResults.group(2)
    r_participant = regResults.group(3)
    r_songTitle = regResults.group(4)
    r_songArtist = regResults.group(5)
    return [ r_showId, r_turn, r_participant, r_songTitle, r_songArtist ]
  return []  


CANDIDATES = candidatesNames
LANGUAGES = []
SONGS = []
SHOW_TYPE = [ 'blinds', 'sing-offs', 'battles', 'half-final', 'final' ]


#STEP: Blinds
lines_sourceBlinds = []
lines_sourceBlinds.extend( getRawSourceLines( 0, 'source_blinds' ) )
blindsFileLines = filter(None, lines_sourceBlinds)
for idxLine, line in enumerate( blindsFileLines ):
  lineList = lineSplitColumns( line )
  participant_name = lineList[2]
  song_title = lineList[3]

  if participant_name not in CANDIDATES_AGES:
    CANDIDATES_AGES[ participant_name ] = -1

  SONG_ITEM = {
    'candidate': participant_name,
    'show': 'blinds',
    'song_infos':  findSongInDeezer( song_title )
  }
  SONGS.append( SONG_ITEM )


#STEP: Battles
lines_sourceBattles = []
lines_sourceBattles.extend( getRawSourceLines( 0, 'source_battles' ) )
lines_sourceBattles.extend( getRawSourceLines( 1, 'source_battles' ) )
lines_sourceBattles.extend( getRawSourceLines( 2, 'source_battles' ) )
lines_sourceBattles.extend( getRawSourceLines( 3, 'source_battles' ) )
battlesFileLines = filter(None, lines_sourceBattles)

battlesGroups = []
teams = 0
for idxLine, line in enumerate( battlesFileLines ):
  if ':' in line:
    battleTeam = []
  elif 'Hier das' in line:
    battlesGroups.append( battleTeam )
  else:
    battleTeam.append( line )

for groupData in battlesGroups:
  #COM: first item is the song infos( name, artist), the rest are the candidates
  songInfo = groupData[0]
  candidates = groupData[1:]
  songName = songInfo.split('"')[1]
  SONGS.extend( [ {"song_infos": findSongInDeezer( songName ), 'show':'battles', "candidate_name": candidate } for candidate in candidates ] )


#STEP: Sing-offs
lines_sourceSingOffs = []
lines_sourceSingOffs.extend( getRawSourceLines( 0, 'source_sing-offs' ) )
lines_sourceSingOffs.extend( getRawSourceLines( 1, 'source_sing-offs' ) )
lines_sourceSingOffs.extend( getRawSourceLines( 2, 'source_sing-offs' ) )
lines_sourceSingOffs.extend( getRawSourceLines( 3, 'source_sing-offs' ) )
singOffsFileLines = filter(None, lines_sourceSingOffs)

singOffsGroups = []
teams = 0
for idxLine, line in enumerate( singOffsFileLines ):
  if '"' in line:
    battleTeam = [ line ]
  elif 'Hier d' in line:
    singOffsGroups.append( battleTeam )
  else:
    battleTeam.append( line )

battlesMasterList = []
for groupData in singOffsGroups:
  #COM: first item is the song infos( name, feat), the rest are the candidates
  songInfo = groupData[0]
  participant_name = groupData[1]
  song_title = songInfo.split('"')[1]
  try:
    dezeerInfo = findSongInDeezer( song_title )
  except:
    print song_title
    dezeerInfo = None
  SONG_ITEM = {
    'candidate_name': participant_name,
    'show': 'sing-offs',
    'song_infos':  dezeerInfo
  }
  SONGS.append( SONG_ITEM )


#STEP: half-final
lines_sourceHalffinal = []
lines_sourceHalffinal.extend( getRawSourceLines(0,'source_half-finals') )
lines_sourceHalffinal.extend( getRawSourceLines(1,'source_half-finals') )
lines_sourceHalffinal.extend( getRawSourceLines(2,'source_half-finals') )
lines_sourceHalffinal.extend( getRawSourceLines(3,'source_half-finals') )
blackList = [ ' ', '' ]
halfFinalFileLines = [ item for item in lines_sourceHalffinal if item not in blackList  ]

candidateSongList = []
iterator = iter(halfFinalFileLines)
for idxLine, line in enumerate( iterator ):
  candidateSongList.append( [line, next(iterator)] )
for idxCS, candidateSongItem in enumerate( candidateSongList ):
  participant_name = candidateSongItem[0]
  song_title = candidateSongItem[1].split(' von ')[0].replace('"','')
  SONG_ITEM = {
    'candidate_name': participant_name,
    'show': 'half-final',
    'song_infos':  findSongInDeezer( song_title )
  }
  SONGS.append( SONG_ITEM )


#STEP: final
lines_sourceFinal = []
lines_sourceFinal.extend( getRawSourceLines( 0, 'source_final' ) )

blackList = [ ' ', '' ]
removeEmptyLines = [ item for item in lines_sourceFinal if item not in blackList  ]
candidateSongList = []
iterator = iter(removeEmptyLines)
for idxLine, line in enumerate( iterator ):
  candidateSongList.append( [line, next(iterator), next(iterator), next(iterator)] )
for idxCS, candidateSongItem in enumerate( candidateSongList ):
  participant_name = candidateSongItem[0]
  def getSongData( _songId ): # 1,2, 3
    song_title = candidateSongItem[ _songId ].split(' von ')[0].split('"')[1]
    deezerData = findSongInDeezer( song_title )
    return {
      'candidate_name': participant_name,
      'show': 'final',
      'song_infos':  deezerData
    }
  SONGS.append( getSongData(1) )
  SONGS.append( getSongData(2) )
  SONGS.append( getSongData(3) )


#STEP: Output collection

df_years = deezerSongs.loc[:]['year'].dropna()
yearMax = df_years[ ~df_years.str.contains('[a-z]+')].max()

outputCollection = {
  'now': 2019,
  'candidates_names' : CANDIDATES,
  'candidates_ages' : CANDIDATES_AGES,
  'num_candidates' : len( CANDIDATES ),
  'languages' : LANGUAGES,
  'performances' : SONGS, 
  'num_performances' : len( SONGS ),
  'show_types' : SHOW_TYPE,
  'deezer-quote':{
    'min': float( deezerSongs.loc[:]['deezer-quote'].min()),
    'max': float(deezerSongs.loc[:]['deezer-quote'].max()),
  },
  'years':{
    'min': deezerSongs.loc[:]['year'].dropna().min(),
    'max': yearMax
  }
}

#STEP: output-file
outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 
outputFilePath = outputPath + config['target']['file'].replace("$VERSION$", str( config['version'] ) )

#com: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )

with open( outputFilePath , 'w') as outfile:
  json.dump( outputCollection , outfile , indent=2, ensure_ascii=False)


#STEP: update config file
yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
