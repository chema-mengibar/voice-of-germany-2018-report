# -*- coding: iso-8859-1 -*-
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

CONFIG_FILE_NAME = '005.01_config'
config = yaml.load( stream = file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'r'))
#yaml.dump( config, file( DIR_TASK + '\\config.yml', 'w') )

sys.path.append( DIR_LIB )

from lib.router import Router
router = Router( )

# --------------------------------------------------------------------------

#STEP: modify version?

configVersion = config['version']
config['version'] =  round( float(configVersion) + .1, 1 ) if config['options']['increment-version'] == True else configVersion

#STEP: load file json
sourcePathFile = router.getRoute( config['source']['route'] ) + config['source']['dir'] + config['source']['file']
rawObj = open( sourcePathFile , 'r')
deezerSongs = json.load( rawObj )


def getExtraInfos( songItem ):
  songName = songItem["song"].replace('\n','')
  songArtist = songItem["artist"].replace('\n','')

  songNameForSeach = songName.replace(' ','+')
  songArtistForSeach = songArtist.replace(' ','+')

  browser = webdriver.Chrome(executable_path=r"..\\lib\\selenium\\chromedriver_1.exe")
  url = 'http://www.google.com'
  params = '/search?&q=' + songNameForSeach + '+' + songArtistForSeach
  browser.get(url + params)
  time.sleep( 0.3 )

  genreText = ''
  genreBox = browser.find_elements_by_xpath('//*[contains(text(), "Genre")]')
  if len(genreBox) > 0:
    rowItem = genreBox[0].find_element_by_xpath('..').find_element_by_xpath('..')
    if len( rowItem.find_elements_by_tag_name('span') ) > 0:
      genreText = rowItem.find_elements_by_tag_name('span')[1].get_attribute('innerText')

  dateText = ''
  dateBox = browser.find_elements_by_xpath('//*[contains(text(), "Veröffentlicht")]')
  if len(dateBox) > 0:
    rowItem = dateBox[0].find_element_by_xpath('..').find_element_by_xpath('..')
    
    if len( rowItem.find_elements_by_tag_name('span') ) > 0:
      dateText = rowItem.find_elements_by_tag_name('span')[1].get_attribute('innerText')
  browser.close()
  return ( genreText, dateText )

# https://stackoverflow.com/questions/24475393/unicodedecodeerror-ascii-codec-cant-decode-byte-0xc3-in-position-23-ordinal

#STEP: output-file

outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 
outputFilePath = outputPath + config['target']['file'].replace("$VERSION$", str( config['version'] ) )

#com: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )

headerRow = [
  'deezer-playlist-id',
  'song',
  'artist',
  'year',
  'genre',
  'deezer-quote'
]

if config['params']['initial'] == True:
  config['params']['initial'] = False
  yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
  with open( outputFilePath ,"w") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=';')
    csvWriter.writerow( headerRow )


startSongId = config['params']['current'] # or 0

for songIdx in range( startSongId, len(deezerSongs)):
  songItem = deezerSongs[ songIdx]
  extraInfos = getExtraInfos( songItem )
  time.sleep( 0.3 )

  deezerSongs[songIdx]["genre"]= extraInfos[0]
  deezerSongs[songIdx]["year"]= extraInfos[1]
  deezerSongs[songIdx]["song"] = deezerSongs[songIdx]["song"].replace('\n','')
  deezerSongs[songIdx]["artist"] = deezerSongs[songIdx]["artist"].replace('\n','')
  deezerSongs[songIdx]["quote"] = deezerSongs[songIdx]["quote"].replace('Popularidad:','').replace(' / 10','')

  rowItem = [
    deezerSongs[songIdx]["cursor"],
    deezerSongs[songIdx]["song"].encode("utf-8") ,
    deezerSongs[songIdx]["artist"].encode("utf-8") ,
    deezerSongs[songIdx]["year"],
    deezerSongs[songIdx]["genre"].encode("utf-8") ,
    deezerSongs[songIdx]["quote"],
  ]

  with open( outputFilePath ,"a") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=';')
    csvWriter.writerow( rowItem )
  
  config['params']['current'] = int( deezerSongs[songIdx]["cursor"] )
  yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )


#STEP: update config file

yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
