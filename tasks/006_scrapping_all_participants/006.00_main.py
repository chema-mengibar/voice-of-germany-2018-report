import os
import sys

DIR_TASK = os.path.basename(os.getcwd())
DIR_LIB = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
DIR_TASK = os.path.dirname(os.path.abspath(__file__))

import json, csv, time, string, itertools, copy, yaml
import numpy as np
import pandas as pd
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

CONFIG_FILE_NAME = '006.00_config'
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

sourcePathFile = router.getRoute( config['source']['route'] ) + config['source']['dir'] + config['source']['file']
rawObj = open( sourcePathFile , 'r')
fileJsonContent = json.load( rawObj )

#STEP: definition
def openPartLink( _part, _coachKey, _partId ):
  params = '' # '/videos?disable_polymer=1'
  url = _part['link']
  browser.get( url  + params )
  # time.sleep( 2 )
  browser.implicitly_wait( 2 )
  iframe = browser.find_elements_by_class_name('htmlcontent')[0]
  browser.switch_to.frame( iframe )

  infoCols = browser.find_elements_by_class_name('talent-detail__facts-col')

  ageField = infoCols[0].find_elements_by_css_selector('p')[1].get_attribute('innerText').encode('utf-8').replace('\n','')
  isAgeInt = isinstance( ageField, int)
  ageValue = int( ageField ) if isAgeInt else ageField
  participantData = {
    'list_pos_participant': _partId,
    'name': _part['name'],
    'coach': _coachKey,
    'age' : ageValue,
    'buzzer': infoCols[1].find_elements_by_css_selector('p')[1].get_attribute('innerText').encode('utf-8').replace('\n',''),
    'song' : infoCols[2].find_elements_by_css_selector('p')[1].get_attribute('innerText').encode('utf-8').replace('\n',''),
    # 'job' : infoCols[3].find_elements_by_css_selector('p')[1].get_attribute('innerText').encode('utf-8').replace('\n','')
  }

  return participantData

def cleanPartData( _partDataObj ):
  _partDataObj["song"] = _partDataObj["song"].replace('"',"'") # @

  buzzerRaw0 = _partDataObj["buzzer"].title().split('(')
  buzzerNum = int( buzzerRaw0[0].strip() )
  buzzerCoachesList = buzzerRaw0[1].replace(')','').split(',')

  _partDataObj["buzzer_count"] = buzzerNum
  _partDataObj["buzzer_coaches"] = [ item.strip() for item in buzzerCoachesList ]

  if 'VON' in _partDataObj["song"]:
    songData =  _partDataObj["song"].split('VON')
  else:
    songData =  _partDataObj["song"].split("' ") # @

  _partDataObj["song_title"] = songData[0].replace("'",'').strip()
  _partDataObj["song_artist"] = songData[1].strip() 
  return _partDataObj

def saveObjFile( _partData ):

  fileName = _partData['name'].replace(' ', '-')

  outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 
  outputFilePath = outputPath + config['target']['file'].replace("$PART$", fileName )

  #com: create output folder
  if not os.path.exists( outputPath ):
    os.makedirs( outputPath )

  with open( outputFilePath, 'w') as outfile:
    json.dump( _partData , outfile , indent=2)

# -------------------------------------------------------------------------

#STEP: define idx of Coach and Participant (idx from file)

coachesList = fileJsonContent.keys()

configParamCoach = config['params']['start_coach']

startCoachId = 0 if configParamCoach == -1 else configParamCoach

for coachId in range( startCoachId , len(coachesList) ):

  coachName = coachesList[ coachId ]

  if coachId == config['params']['start_coach'] :
    startPartId = config['params']['start_part'] 
  else: 
    startPartId = 0

  for partIdx in range( startPartId, len( fileJsonContent[ coachName ] ) ):
    browser = webdriver.Chrome(executable_path=r"..\\lib\\selenium\\chromedriver_1.exe")
    part = fileJsonContent[ coachName ][partIdx]

    print( coachName, partIdx )
    #STEP: Init
    partDataObj = openPartLink( part, coachName, partIdx )
    partDataObjMod = cleanPartData( partDataObj )
    saveObjFile( partDataObjMod )

    #STEP: close
    browser.close();

