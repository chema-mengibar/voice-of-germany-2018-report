import os
import sys

from os import listdir
from os.path import isfile, join

DIR_TASK = os.path.basename(os.getcwd())
DIR_LIB = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
DIR_TASK = os.path.dirname(os.path.abspath(__file__))

import json, csv, time, string, itertools, copy, yaml
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors


CONFIG_FILE_NAME = '002.01_config'
config = yaml.load( stream = file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'r'))
#yaml.dump( config, file( DIR_TASK + '\\config.yml', 'w') )

sys.path.append( DIR_LIB )

from lib.router import Router
router = Router( )
print '>> Walk, Don`t Run'
# --------------------------------------------------------------------------
#STEP: modify version?

configVersion = config['version']
config['version'] =  round( float(configVersion) + .1, 1 ) if config['options']['increment-version'] == True else configVersion


#STEP: prepare Plot
plt.xlabel( 'xLabel' )
plt.ylabel( "yLabel" )

#STEP: load
sourcePath = router.getRoute( config['source']['route'] ) + config['source']['dir'] + config['source']['file']
rawObj = open( sourcePath, 'r')
fileJsonContent = json.load( rawObj )

colors = {
'ducados':'#1b4079',
'carmin':'#a5243d',
'yema':'#f3a712',
'chocolate':'#534d41',
'purpura':'#5d2e46',
'lila':'#b58db6',
'naranja':'#ff4a1c',
'menta':'#b2ffa9',
'verde':'#06d6a0',
'anyil':'#457b9d',
'beis':'#f7c59f',
'rosa':'#ff92c2'
}

counter = 0
for participantName, participantItem in fileJsonContent.items():
    participantDates =  participantItem.keys()
    participantDatesSorted = sorted( participantDates, key=lambda x: dt.datetime.strptime(x, '%Y-%m-%d'), reverse=False)
    pX = range( 0, len(participantDatesSorted) )
    lX = participantDatesSorted
    pY = [ participantItem[ dateKey ][0]["likes"] for dateKey in participantDatesSorted ]

    pIn = [ participantItem[ dateKey ][0]["in"] for dateKey in participantDatesSorted ]
    participantMin = min(pY)
    participantMax = max(pY)
    lineColor = '#eeeeee'
    labelText = ''
    if ( False not in pIn): # and participantMax > 5000:
        lineColor = colors.items()[counter][1]
        labelText = participantName
        counter += 1
    #STEP: Participant Plot
    # plt.xticks(pX, lX, rotation=90)
    if False not in pIn:
        plt.plot( pX, pY, color=lineColor, label=labelText)

#plt.legend([participantLine01], ['Line Up'])
plt.legend( bbox_to_anchor=(0., 1.02, 1., .102), loc=3,  ncol=2, mode="expand", borderaxespad=0. )

#STEP: output-file
#COM: Absolute Path
outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir']
outputFilePath = outputPath + config['target']['file'].replace("$VERSION$", str( config['version'] ) )

plt.savefig( outputFilePath, bbox_inches='tight')

#COM: create output file


#STEP: update config file
yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
