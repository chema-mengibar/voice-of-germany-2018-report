# -*- coding: utf-8 -*-
import os
import sys

DIR_TASK = os.path.basename(os.getcwd())
DIR_LIB = os.path.abspath(os.path.join(os.path.dirname(__file__),'../'))
DIR_TASK = os.path.dirname(os.path.abspath(__file__))

import json, csv, time, string, itertools, copy, yaml
import numpy as np
import pandas as pd
import datetime as dt

CONFIG_FILE_NAME = '011-R.00_config'
config = yaml.load( stream = file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'r'))
#yaml.dump( config, file( DIR_TASK + '\\config.yml', 'w') )

sys.path.append( DIR_LIB )

from lib.router import Router
router = Router( )

# --------------------------------------------------------------------------
today = dt.datetime.now().strftime('%Y-%m-%d--%H-%M') 

#DEF:
def getSourceFile( _sourceKey, _fileIdx ):
  sourceName = config['source'][ _sourceKey ]
  sourcePathFile = router.getRoute( sourceName['route'] ) + sourceName['dir'] + sourceName['files'][ _fileIdx ]
  return open( sourcePathFile , 'r')


#STEP: modify version?
configVersion = config['version']
config['version'] =  round( float(configVersion) + .1, 1 ) if config['options']['increment-version'] == True else configVersion
CONFIG_INCLUDE_FINAL = config['params']['include_final']['value']

#STEP: load files
#com: performances
rawContent = getSourceFile( 'source_langs', 0 )  
fileJsonContent = json.load( rawContent )

#com: show quotes
quotesFileSemiFinal = getSourceFile( 'source_quotes', 0 ) 
df_quotesSemifinal = pd.read_csv( filepath_or_buffer=quotesFileSemiFinal, sep=";", quoting=3, decimal="," )

quotesFileFinal = getSourceFile( 'source_quotes', 1 ) 
df_quotesFinal = pd.read_csv( filepath_or_buffer=quotesFileFinal, sep=";", quoting=3, decimal="," )

def strToKey( _string ):
  #com: change character case to lower, replace spaces to underscore
  jsonKey = _string.lower().replace(' ', '_')
  return jsonKey

#STEP:
names =  fileJsonContent['candidates_names']
#com: List for each candidate to save the lang songs
songsByCandidate = {}
for name in names:
  #com: box-list by candidate for the language keys
  songsByCandidate[ strToKey(name) ] = {
    'langs':[],
    'name': name,
    'is_finalist':False, 
    'is_semifinalist':False
  } 


#STEP: Add the performance infos to the candidate list: is semi/finalist and the list of song-languages-keys  til semifinal show.
performances = fileJsonContent['performances']
for performance in performances:
  performer = performance['candidate_name'] if 'candidate_name' in performance else performance['candidate']
  performerKey = strToKey(performer)
  langPerformance = performance['song_infos']['lang']
  #com: get languages just for buzzered candidates: more perfomnaces (blinds, etc..) than buzzered candidates
  #com: Karnaugh approach to append candidate infos ->  y = AC' + AB
  A = performerKey in songsByCandidate
  B = CONFIG_INCLUDE_FINAL
  C = performance['show'] == 'final'
  if A and not C or A and B :
    songsByCandidate[ performerKey ]['langs'].append( langPerformance )

  if performance['show'] == 'half-final':
    songsByCandidate[ performerKey ]['is_semifinalist'] = True
  
  if performance['show'] == 'final':
    songsByCandidate[ performerKey ]['is_finalist'] = True


#STEP: Calculate languages rates
def countLangKeys( _listLangs ):
  #com: ['de','en','en'] -> {'de':1, 'en':2}
  langKeys = set( _listLangs )
  resultRates = []
  for langKey in langKeys:
    langValue = _listLangs.count( langKey )
    resultRates.append( { '_key': langKey , '_value': langValue   } )
  return resultRates
   
    
def rateLangKeys( _listLangs ):
  #com: ['de','en','en'] -> {'de':33.33, 'en':66.66}
  langKeys = set( _listLangs )
  numSongs = len( _listLangs )
  resultRates = []
  for langKey in langKeys:
    langValue = round( float(_listLangs.count( langKey ) * 100 ) / numSongs , 2)
    resultRates.append( { '_key': langKey , '_value': langValue, '_symbol':'%'} )
  return resultRates

#com: Calculate for all the candidates
taskDataList = []
for candidateName in songsByCandidate.keys():
  listLangs = songsByCandidate[ candidateName ]['langs']
  #HELP: 'quote_final': df_quotesFinal.loc[ df_quotesFinal.participant == name ]['rate_procent'].values[0],
  #HELP: 'quote_semifinal': df_quotesSemifinal.loc[ df_quotesSemifinal.participant == name ]['rate_procent'].values[0]
  #HELP: 'is_finalist':  songsByCandidate[ candidateName ]['is_finalist'],
  #ADV:  mode -> is_semifinalist or is_finalist

  candidateBuffer = {}
  realName = songsByCandidate[ candidateName ]['name']

  if songsByCandidate[ candidateName ]['is_semifinalist']:
    isWinner = True if df_quotesSemifinal.loc[ df_quotesSemifinal.participant == realName.encode('utf-8') ]['winner'].values[0] == '+' else False
    candidateBuffer['candidate_name'] = realName.encode('utf-8')
    candidateBuffer['lang_counter'] = countLangKeys( listLangs )
    candidateBuffer['lang_rate'] = rateLangKeys( listLangs )
    candidateBuffer['num_songs'] = len(listLangs)
    candidateBuffer['is_semifinalist'] = songsByCandidate[ candidateName ]['is_semifinalist']
    candidateBuffer['is_semifinalist_winner'] = isWinner
    candidateBuffer['quote_semifinal'] = round( float(df_quotesSemifinal.loc[ df_quotesSemifinal.participant == realName.encode('utf-8') ]['rate_procent'].values[0]),2)
    candidateBuffer['is_finalist'] = songsByCandidate[ candidateName ]['is_finalist']

  if songsByCandidate[ candidateName ]['is_finalist']:
    isWinner = True if df_quotesFinal.loc[ df_quotesFinal.participant == realName.encode('utf-8') ]['winner'].values[0] == '+' else False
    candidateBuffer['is_finalist_winner'] = isWinner
    candidateBuffer['quote_final'] = round( float(df_quotesFinal.loc[ df_quotesFinal.participant == realName.encode('utf-8') ]['rate_procent'].values[0]),2)

  if candidateBuffer:
    taskDataList.append( candidateBuffer )


#STEP: output-file
prefix = '_show-final_' if CONFIG_INCLUDE_FINAL else '_show-semifinal_'
outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 
outputFilePath = outputPath + config['target']['file'].replace('$VERSION$', prefix + str( config['version'] ) )

#com: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )

#com: save taks-data file
with open( outputFilePath , 'w') as outfile:
  json.dump( taskDataList , outfile , indent=2, ensure_ascii=False)


#STEP: update config file
yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
