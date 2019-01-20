#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import time
import datetime as dt
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
os.chdir(os.path.dirname(__file__))

browser = webdriver.Chrome(executable_path=r".\chromedriver.exe")

today = dt.datetime.today()
today = dt.datetime.strftime(today, '%Y.%b.%d')
data_dir ="./capture/"
filename = today + "_tvog__youtube" + '.html'

#candidate = 'Natia+Todua'
candidate = 'Anna+Heimrath'
#candidate = 'BB+Thomaz'
#candidate = 'Benedikt+Köstler'

url = 'https://www.youtube.com/results'
param = '?search_query=' + candidate

browser.get(url + param)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

#channelContent = browser.find_elements_by_id("contents")[0]  #.get_attribute('innerHTML')
# print channelContent.get_attribute('innerHTML').encode("utf-8")
videos =  browser.find_elements_by_class_name("ytd-video-renderer")

print len( videos )

actualItem = []

for idx,item in enumerate(videos):
    # #print item.get_attribute('innerHTML').encode('utf-8')
    try:
        t = item.find_elements_by_xpath("//a[@id='video-title']")[idx].get_attribute('title')
        c = item.find_elements_by_xpath("//div[@id='metadata-line']//span[1]")[idx].get_attribute('innerHTML')
        title =  t.encode('utf-8')
        if( "2017" in title ):
            data = {
                "title": title,
                "likes": int( c.encode('utf-8').replace("Tsd.", "000").split(" ")[0].replace(",", "").replace("&nbsp", "").replace(";", "")  )
            }
            actualItem.append( data )

        print '--------------------'
        #
    except IndexError:
        break
    # c = item.find_elements_by_xpath("//ul[@class='yt-lockup-meta-info']//li[2]")[idx].get_attribute('innerHTML')
    # #c = item.find_elements_by_class_name("")[idx]


print actualItem
with open('./capture/tvog_youtube_' + candidate + '.json', 'w') as outfile:
    json.dump(actualItem, outfile, ensure_ascii=False)
