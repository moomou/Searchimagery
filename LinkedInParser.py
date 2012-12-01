from Callable import Callable
from google.appengine.api import urlfetch
from bs4 import BeautifulSoup as BS

import SearchVizLib

class LinkedInParser:
    def __init__(self):
        self.enabled = True

    def parseCard(self, soup, options, url):
        content = ''

        infoBox = soup.select('.masthead')
        if not infoBox: #did not find one
            return None
        
        infoBox = infoBox[0]

        content += str(infoBox) 
        return content 

    def parseSkills(self, soup, options, url):
        content = ''

        skillList = soup.select('.skills');

        if not skillList: #did not find one
            return None
        
        skillList = skillList[0]  
        content += str(skillList)
        return content 

    def parseOverview(self, soup, options, url):
        content = ''
        resume = soup.select('.hresume')

        if not resume:
            return None

        resume = resume[0]
        overview = resume.select('#overview')[0] 
        content += str(overview)

        return content

    def getSummary(self,soup, options, url):
        content = ''
        
        card = self.parseCard(soup, options, url)
        skill = self.parseSkills(soup, options, url)
        overview = self.parseOverview(soup, options, url)

        if card: content += card
        if skill: content += skill
        if overview: content += overview

        return {'color':'','size': 'medium','content':content}#.encode('utf-8')

    def loadContent(rpc, threadQueue, url):
        self = LinkedInParser()
        try:
            result = requests.get(url)

            if result.status_code == 200:
                text = result.content
                soup = BS(text)         

                content = self.getSummary(soup, {}, url) 
                if content: threadQueue.append(content)

        except urlfetch.DownloadError: #failed or timed out
            return None 
    loadContent = Callable(loadContent)

    def getName():
        return "linkedin"
    getName = Callable(getName)

