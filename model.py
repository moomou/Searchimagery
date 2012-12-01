from google.appengine.ext import db
from Callable import Callable

class DataStoreWrapper:
    def __init__(self):
        pass

    def search(dbClass, filters):
        q = dbClass.all()
        for key,value in filters.items():
            q.filter(key+' =', value)

        return q.get()
    search = Callable(search)

class SearchEntry(db.Model):
    searchEntity = db.StringProperty()
    searchTerm = db.StringProperty()
    date = db.DateTimeProperty()

class Picograph(db.Model):
    searchEntry = db.ReferenceProperty(SearchEntry,
                                      collection_name='picographs')
    srcUrl = db.LinkProperty()
    funcName = db.StringProperty()

    title = db.StringProperty()
    content = db.TextProperty()

    rating = db.RatingProperty()
    date = db.DateTimeProperty()

class CoverImage(db.Model):
    pico = db.ReferenceProperty(Picograph,
                                collection_name='coverImage')
    coverId = db.StringProperty()
    src = db.LinkProperty()
    rating = db.RatingProperty()
