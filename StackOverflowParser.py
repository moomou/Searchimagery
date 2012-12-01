from Callable import Callable
from google.appengine.api import urlfetch
from bs4 import BeautifulSoup as BS

import logging
import SearchVizLib

class StackOverflowParser:
    def __init__(self):
        self.enabled = True

    def parseQuestion(self, soup, options, url):
        content = ''

        question = soup.select('#question')
        if not question: #did not find one
            return None
        
        question = question[0]
        qContent, qComment = question.table.find('tr')
        #not using comment for now
        content += str(qContent) 

        return {'color':'','size': 'medium','content':content}#.encode('utf-8')

    def parseAnswer(self, soup, options, url):
        content = ''

        answer = soup.select('.answer');
        if not answer: #did not find one
            return None
        
        answer = answer[0] #selecting the first answer 
        answer = answer.table.find('tr')
        content += str(answer)

        return {'color':'','size': 'medium','content':content}#.encode('utf-8')

    def loadContent(rpc, threadQueue, url):
        self = StackOverflowParser()
        try:
            #result = rpc.get_result()
            result = rpc(url)

            if result:
                logging.info('StackOverflow loaded') 
                text = result#.content
                soup = BS(text)         

                content = self.parseQuestion(soup, {}, url) 
                if content: threadQueue.append(content)

                content = self.parseAnswer(soup, {}, url) 
                if content: threadQueue.append(content)
            else:
                logging.info('StackOverflow failure code') 

        except urlfetch.DownloadError: #failed or timed out
            logging.error('StackOverflow load failed') 
            return None 
    loadContent = Callable(loadContent)
    
    #Must have methods
    def getRemaining():
        pass
    getRemaining = Callable(getRemaining)

    def render(URLs,options,url):
        pass
    render = Callable(render)
