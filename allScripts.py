from WikiParser import WikiParser
from JLyricParser import JLyricParser 

import sys, inspect, logging

LOAD_CONTENT = "loadContent"

class AllScripts:
    def __init__(self):
        self.scripts = {}
        currentModule = sys.modules[__name__]
        clsmembers = inspect.getmembers(currentModule, inspect.isclass)

        for member in clsmembers: 
            if (member[0].lower().find("parser") > -1):
                name = member[0]
                obj = member[1]
                self.scripts[obj.getName()] = obj.__dict__[LOAD_CONTENT]
