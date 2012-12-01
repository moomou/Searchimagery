import requests
import json

class Geolocation:
    def __init__(self):
        self.url = 'http://freegeoip.net/json/'
    def lookup(self,ip):
        result = requests.get(self.url+ip)
        if result.status_code == 200: 
            return json.loads(result.text)
        else: 
            return None        
        
