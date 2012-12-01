#Youtube Search
from bs4 import BeautifulSoup as BS
import requests
import gdata.youtube
import gdata.youtube.service
import logging,pprint

class YtubeSearch:
    def __init__(self, searchTerms, categoryTerms):
        logging.info("YPaser s: %s c: %s" %(searchTerms, categoryTerms)) 
        self.searchTerm = searchTerms
        self.categoryTerm = categoryTerms
        keywords = searchTerms+" "+categoryTerms
        #self.videoListWithMetaData = self.SearchAndPrintVideosByKeywords(keywords)
        #self.video = self.SearchAndPrint(searchTerms)
        self.playListSearchResult = self.SearchPlaylist(searchTerms)  

    def getTopPlaylist(self):
        return self.playListSearchResult

    def getVideoListWithMetaData(self): 
        #return self.videoListWithMetaData
        return self.video

    def createJSONData(self,feed):
        videoListWithMetaData = []

        for entry in feed.entry:
            if not entry:
                continue
            if entry.rating.num_raters < 1000:
                continue

            videoEntry = {}
            logging.info(pprint.pprint(entry.__dict__))
            
            videoEntry['title'] = entry.title.text
            videoEntry['videoID'] = entry.id.text.split('/')[-1]
            videoEntry['rating'] = entry.rating.average
            videoEntry['numRaters'] = entry.rating.num_raters
            videoEntry['keywords'] = entry.media.keywords.text
            videoEntry['date'] = entry.published.text.split('T')[0]
            #many more could be added
            videoListWithMetaData.append(videoEntry)

        return videoListWithMetaData
        
    def SearchAndPrint(self,search_terms):
        yt_service = gdata.youtube.service.YouTubeService()
        query = gdata.youtube.service.YouTubeVideoQuery()
        query.vq = search_terms
        query.genre = 16 #entertainment
        query.orderby = 'rating'
        query.racy = 'exclude'

        feed = yt_service.YouTubeQuery(query)
        videoListWithMetaData = self.createJSONData(feed) 

        return videoListWithMetaData

    def SearchAndPrintVideosByKeywords(self,keywords, orderBy='rating', racy="include"):
        yt_service = gdata.youtube.service.YouTubeService()
        query = gdata.youtube.service.YouTubeVideoQuery()

        query.orderby = 'rating'  
        query.racy = racy

        for search_term in keywords.split(" "):
          new_term = search_term.lower()
          query.categories.append('/%s' % new_term)

        feed = yt_service.YouTubeQuery(query)
        videoListWithMetaData = self.createJSONData(feed) 

        return videoListWithMetaData
    
    def SearchPlaylist(self, keywords):
        yt_service = gdata.youtube.service.YouTubeService()
        PlayListURL = "http://gdata.youtube.com/feeds/api/playlists/snippets?v=2&q="

        for search_term in keywords.split(" "):
          new_term = search_term.lower()
          PlayListURL += search_term+"%20" 

        result = requests.get(PlayListURL)

        if (result.status_code == 200):
            soup = BS(result.text)
        else:
            logging.error('GOOG...')

        listEntry = [] 
        for entry in soup.findAll('entry'):
            countHint = entry.find('yt:counthint').text
            playlistId = entry.find('yt:playlistid').text
            listEntry.append({'count':countHint,'id':playlistId}) 
        listEntry.sort()

        return listEntry 
