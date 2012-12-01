from bs4 import BeautifulSoup as BS
import logging
import urllib,urllib2
import requests
import ssl
import chardet
import re
from geolcation import Geolocation
from YoutubeSearch import YtubeSearch 
from bing import Bing
b = Bing()
print b.searchWeb('akb',{'location':'JP'})
#jgeo = Geolocation()
#print geo.lookup('129.97.224.225')
'''
re.compile = r'/\[(.*?)\]/'
url1 = "http://en.wikipedia.org/wiki/Tom_cruise"
url2 = "http://en.wikipedia.org/wiki/Cat"
#result = requests.get(url2)

f = open('fake.html')
soup = BS(f)
cont = str(soup.p)
print type(cont)
print type(u'abc')
print type(u'abc'.encode('ascii'))
print type(u'abc'+'abc')

soup = BS(result.text)
ps = []
content = ''

for child in soup.select('#mw-content-text')[0].contents:
    if hasattr(child,'name'):
        if child.name == "p":
            ps.append(child)

img = '<img src="'+u'abc'+'"></img>' 
img = img.encode('utf-8')
content = img + "<br>".join([str(t) for t in ps])

PlayListURL = "https://gdata.youtube.com/feeds/api/playlists/snippets?v=2&q="

tmp = YtubeSearch('cat','music')
print tmp.playListSearchResult.get
print tmp.SearchAndPrintVideosByKeywords('cat')
'''
