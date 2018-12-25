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

config = yaml.load( stream = file( DIR_TASK + '\\config_001.00.yml', 'r'))
#yaml.dump( config, file( DIR_TASK + '\\config.yml', 'w') )

sys.path.append( DIR_LIB )

from lib.router import Router
router = Router( )

print 'walk, don`t run'
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

seq = browser.find_elements_by_tag_name('iframe')
print("Frames present in the web page are: ", len(seq))

browser.switch_to_default_content()
iframe = browser.find_elements_by_tag_name('iframe')[0]
browser.switch_to.frame(iframe)
browser.implicitly_wait(5)

coaches = browser.find_elements_by_class_name("team-filter__item")

# links = []

teamsData = {}
for cIdx, cItem in enumerate( coaches ):
  coach = coaches[ cIdx ]
  coachName =  coach.get_attribute('data-team-name').encode('utf-8')
  coach.click()

  teamsData[ coachName ] = []

  browser.implicitly_wait(5)

  rowTalents = browser.find_elements_by_class_name("talent-teaser")
  for idx,item in enumerate( rowTalents ):
    itemClass = item.get_attribute('class')
    participantIn = False if 'out' in itemClass else True
    participantName = item.find_element_by_class_name("talent-teaser__name").get_attribute('innerHTML')
    participantLink = item.find_element_by_class_name("talent-teaser__link").get_attribute('href')
    participantLikes =  int( item.find_element_by_class_name("like__label").get_attribute('innerHTML') )

    # links.append( participantLink )

    participantData = {
      'in': participantIn,
      'name' : participantName.encode('utf-8'),
      'likes': participantLikes,
      'link' : participantLink.encode('utf-8')
    }
    teamsData[ coachName ].append( participantData )


#STEP: output-file

outputPath =  router.getRoute( config['target']['route'] ) \
+ config['target']['dir'] \

#com: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )

outputFilePath = outputPath \
+ config['target']['file'].replace("$TIME$", today )

with open( outputFilePath, 'w') as outfile:
  json.dump( teamsData , outfile , indent=2)



# outputFilePath = outputPath \
# + config['target']['file_links'].replace("$TIME$", today )

# with open( outputFilePath, 'w') as outfile:
#   json.dump( links , outfile , indent=2)