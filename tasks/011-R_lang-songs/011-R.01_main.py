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

CONFIG_FILE_NAME = '011-R.01_config'
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


#STEP: load files
#com: performances
rawContent = getSourceFile( 'source_langs', 0 )  
fileJsonContent = json.load( rawContent )

#com: show quotes
quotesFileSemiFinal = getSourceFile( 'source_quotes', 0 ) 
df_quotesSemifinal = pd.read_csv( filepath_or_buffer=quotesFileSemiFinal, sep=";", quoting=3, decimal="," )

quotesFileFinal = getSourceFile( 'source_quotes', 1 ) 
df_quotesFinal = pd.read_csv( filepath_or_buffer=quotesFileFinal, sep=";", quoting=3, decimal="," )


#STEP:
names =  fileJsonContent['candidates_names']
#com: List for each candidate to save the lang songs
nextRoundsCandidates = {}
for name in names:
  #com: box-list by candidate for the language keys
  nextRoundsCandidates[ name ] = {
    'is_finalist':False, 
    'is_semifinalist':False
  } 

#STEP:
performances = fileJsonContent['performances']
for performance in performances:
  performer = performance['candidate_name'] if 'candidate_name' in performance else performance['candidate']

  #com: remove the non-buzzered candidates
  if performer in nextRoundsCandidates:
    nextRoundsCandidates[ performer ]['song'] = performance['song_infos']['title']
    nextRoundsCandidates[ performer ]['deezer_quote'] = performance['song_infos']['deezer_quote']
    if performance['show'] == 'half-final':
      nextRoundsCandidates[ performer ]['is_semifinalist'] = True
    
    if performance['show'] == 'final':
      nextRoundsCandidates[ performer ]['is_finalist'] = True


taskDataList_semifinal = []
for candidateName in nextRoundsCandidates.keys():
  candidateBuffer = {}
  if nextRoundsCandidates[ candidateName ]['is_semifinalist']:

    quoteDeezer = nextRoundsCandidates[ candidateName ]['deezer_quote']
    quoteVotes = round( float(df_quotesSemifinal.loc[ df_quotesSemifinal.participant == candidateName.encode('utf-8') ]['rate_procent'].values[0]),2)
    relationSemifinal = int( quoteDeezer*10 - quoteVotes )

    isWinner = True if df_quotesSemifinal.loc[ df_quotesSemifinal.participant == candidateName.encode('utf-8') ]['winner'].values[0] == '+' else False
    candidateBuffer['candidate_name'] = candidateName.encode('utf-8')
    candidateBuffer['is_semifinalist'] = nextRoundsCandidates[ candidateName ]['is_semifinalist']
    candidateBuffer['is_semifinalist_winner'] = isWinner
    candidateBuffer['song'] = nextRoundsCandidates[ candidateName ]['song'].encode('utf-8')
    candidateBuffer['deezer_quote'] = quoteDeezer
    candidateBuffer['quote_semifinal'] = quoteVotes
    candidateBuffer['relation_semifinal'] = relationSemifinal
  if candidateBuffer:
    taskDataList_semifinal.append( candidateBuffer )  


taskDataList_final = []
for candidateName in nextRoundsCandidates.keys():
  candidateBuffer = {}
  if nextRoundsCandidates[ candidateName ]['is_finalist']:

    quoteDeezer = nextRoundsCandidates[ candidateName ]['deezer_quote']
    quoteVotes = round( float(df_quotesFinal.loc[ df_quotesFinal.participant == candidateName.encode('utf-8') ]['rate_procent'].values[0]),2)
    relationFinal = int( quoteDeezer*10 - quoteVotes )

    isWinner = True if df_quotesFinal.loc[ df_quotesFinal.participant == candidateName.encode('utf-8') ]['winner'].values[0] == '+' else False
    candidateBuffer['candidate_name'] = candidateName.encode('utf-8')
    candidateBuffer['is_finalist'] = nextRoundsCandidates[ candidateName ]['is_finalist']
    candidateBuffer['is_finalist_winner'] = isWinner
    candidateBuffer['song'] = nextRoundsCandidates[ candidateName ]['song'].encode('utf-8')
    candidateBuffer['deezer_quote'] = quoteDeezer
    candidateBuffer['quote_final'] = quoteVotes
    candidateBuffer['relation_final'] = relationFinal
  if candidateBuffer:
    taskDataList_final.append( candidateBuffer )  






#STEP: output-file
outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 


#com: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )

#com: save taks-data file -> SEMIFINAL
outputFilePath = outputPath + config['target']['file'].replace('$VERSION$', '_semifinal_' + str( config['version'] ) )
with open( outputFilePath , 'w') as outfile:
  json.dump( taskDataList_semifinal , outfile , indent=2, ensure_ascii=False)

#com: save taks-data file -> FINAL
outputFilePath = outputPath + config['target']['file'].replace('$VERSION$', '_final_' + str( config['version'] ) )
with open( outputFilePath , 'w') as outfile:
  json.dump( taskDataList_final , outfile , indent=2, ensure_ascii=False)

#STEP: update config file
yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
