COMMON_WEB = [{'site':/.*wiki.*/,
                'func': 'WikiParser.loadContent'},
                {'site':/.*linkedin.*/,
                'func': 'LinkedInParser.loadContent'},
                {'site':/.*stackoverflow.*/,
                'func': 'StackOverflowParser.loadContent'},
                {'site':/.*j-lyric.*/,
                'func': 'JLyricParser.loadContent'}]
