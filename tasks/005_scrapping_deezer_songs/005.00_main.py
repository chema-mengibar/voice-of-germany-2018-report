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

CONFIG_FILE_NAME = '005.00_config'
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


#STEP: web-load 

browser = webdriver.Chrome(executable_path=r"..\\lib\\selenium\\chromedriver_1.exe")
#browser = webdriver.Chrome(executable_path= DIR_LIB + "chromedriver.exe")

url = config['params']['url']
params = '' # '/videos?disable_polymer=1'
browser.get(url + params)
time.sleep( 2 )

# Step: close cookies pop-up
cookiesArea = browser.find_element_by_class_name("cookie-right")
cookiesArea.find_element_by_class_name("btn-primary").click()

body = browser.find_element_by_tag_name("body")
deezerData = []
idsData = []


# STEP: the loop-catch fct

def moveDown( _numMoves):
  for n in range(0,_numMoves):
    body.send_keys(Keys.DOWN)
    time.sleep(0.1)

def moveUp( _numMoves):
  for n in range(0,_numMoves):
    body.send_keys(Keys.UP)
    time.sleep(0.1)

def getCurrentRows( _cursor ):
  try:
    subItem = browser.find_elements_by_xpath('//*[@class="datagrid-track-number"][contains(text(), "' + str(_cursor) + '")]')
    if len(subItem) >= 0 :
      rowItem = subItem[0].find_element_by_xpath('..').find_element_by_xpath('..')
      
      popularityItem = rowItem.find_element_by_class_name('popularity-note')
      hover = ActionChains(browser).move_to_element( popularityItem ).perform()
      quoteText = browser.find_element_by_class_name("tooltip-left").get_attribute('innerHTML')
      
      artistText = rowItem.find_element_by_class_name('cell-artist').get_attribute('innerText').encode('utf-8')
      songText = rowItem.find_element_by_class_name('cell-title').get_attribute('innerText').encode('utf-8')
      # artistText = rowItem.find_element_by_xpath('//a[@itemprop="byArtist"]').get_attribute('innerHTML').encode('utf-8') #INFO: doesn`t work
      # songText = rowItem.find_element_by_xpath('//span[@itemprop="name"]').get_attribute('innerHTML').encode('utf-8')
      #dataKey = rowItem.get_attribute('data-key')
      elementData = { "cursor": str(_cursor) ,"quote": quoteText, "artist": artistText, "song": songText }
      deezerData.append( elementData )
      return True
    else:
      return False
  except NoSuchElementException:
    return False
    print("No element found")


# STEP: scroll till end to get the total num of items
continueScroll = True
size_before = body.size["height"]
size_after = 0
step = 1

while continueScroll:
  body.send_keys(Keys.PAGE_DOWN)
  time.sleep(0.3)
  size_after = body.size["height"]
  if step > 10:
      print '>> scrolling'
      step=0
      if(size_before == size_after):
          continueScroll = False
          print '>> End Page'
      else:
          size_before = size_after
  step+=1

songsRows = browser.find_elements_by_class_name("datagrid-row")
numTotalItems = int( songsRows[-1].find_element_by_class_name("datagrid-track-number").get_attribute('innerHTML').encode('utf-8') )


# STEP: scroll to the top again
headerItem = browser.find_element_by_class_name("datagrid-header")
hover = ActionChains(browser).move_to_element( headerItem ).perform()
time.sleep( 1 )


# STEP: the loop
continueScroll = True
cursor = 1

while continueScroll:
  print( cursor, numTotalItems )
  if( cursor > numTotalItems ):
    continueScroll = False
  else:  
    hasFoundItem = getCurrentRows( cursor )
    if( hasFoundItem ):
      moveDown( 1 )
      cursor +=1
    else:
      moveDown( 12 )


# #STEP: output-file

outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 
outputFilePath = outputPath + config['target']['file'].replace("$TIME$", str( today ) )

#com: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )

with open( outputFilePath, 'w') as outfile:
  json.dump( deezerData , outfile , indent=2)


#STEP: update config file

yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
