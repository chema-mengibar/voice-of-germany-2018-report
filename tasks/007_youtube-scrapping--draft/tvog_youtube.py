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
url = 'https://www.youtube.com/user/VoiceOfGermanyTVOG'
param = '/videos?disable_polymer=1'

browser.get(url + param)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

channelContent = browser.find_elements_by_class_name("branded-page-v2-body")[0]#.get_attribute('innerHTML')
videos =  channelContent.find_elements_by_class_name("channels-content-item")

actualItem = []

for idx,item in enumerate(videos):
    #print item.get_attribute('innerHTML').encode('utf-8')
    t = item.find_elements_by_xpath("//h3/a")[idx].get_attribute('title')
    c = item.find_elements_by_xpath("//ul[@class='yt-lockup-meta-info']//li[1]")[idx].get_attribute('innerHTML')
    #c = item.find_elements_by_class_name("")[idx]
    title =  t.encode('utf-8')
    print c.encode('utf-8')
    if( "2017" in title ):
        data = {
            "title": title,
            "likes": int( c.encode('utf-8').split(" ")[0].replace(".", "")  )
        }
        actualItem.append( data )

    print '--------------------'

print actualItem
with open('./capture/tvog_channel.json', 'w') as outfile:
    json.dump(actualItem, outfile, ensure_ascii=False)
