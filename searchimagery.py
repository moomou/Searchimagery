from Callable import Callable
from collections import deque
from allScripts import AllScripts

import requests, sys, inspect, threading, Queue, logging

allScripts = AllScripts()

class Searchimagery:
    def __init__(self,URL):
        pass

    def loadURL(url):
        result = requests.get(url)
        return result
    loadURL = Callable(loadURL)

class ScriptEngine:
    def getCmd(scriptClass, scriptFunc): 
        pass

    def exeAll(query, urls, channelName, searchType=""):
        #logging.error(urls)
        for domainName in urls['web']['ranking']:
            if domainName in allScripts.scripts: #contains scripts for 
                ScriptEngine.exe(query,
                                 allScripts.scripts[domainName],
                                 urls['web']['ranking'][domainName],
                                 urls['image']['url'],
                                 channelName)
    exeAll = Callable(exeAll)

    def exe(query, scriptFunc,URLLists, imageURL, channelName):
        for url in URLLists:
            asyncURLLoad = Searchimagery.loadURL
            thread = threading.Thread(target=scriptFunc,
                                      args=[query,
                                            asyncURLLoad,
                                            url,
                                            imageURL, 
                                            channelName]) 
            thread.start()
    exe = Callable(exe)
