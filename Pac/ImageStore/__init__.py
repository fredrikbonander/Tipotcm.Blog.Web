from Pac.DataFactory import dbImageStore
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache
from google.appengine.ext.webapp import blobstore_handlers
from Pac import Settings
from google.appengine.ext.db import KindError

class AddUpdateImageStore(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        if self.request.get('imagestore_key'):
            image = dbImageStore.ImageStore.get(self.request.get('imagestore_key'))
        else:
            image = dbImageStore.ImageStore()
            
        image.name = self.request.get('image_name')
        image.imageReferance = self.request.get('image_referance')
        
        upload_files =  self.get_uploads('image_file')
        
        if upload_files:
            image.imageUrl = images.get_serving_url(str(upload_files[0].key()))
        
        imageKey = db.put(image)
    
        for market in Settings.markets:
            language = market['language']
            description = self.request.get('image_description_' + language)
            if description:
                imageDescription = dbImageStore.ImageDescription.gql('WHERE imageEntry = :imageEntry AND lang = :lang', imageEntry = imageKey, lang = language).get()
                if imageDescription is None:
                    imageDescription = dbImageStore.ImageDescription()
                    imageDescription.imageEntry = imageKey
                    imageDescription.lang = language
                
                imageDescription.description = description
                db.put(imageDescription)
    
        self.redirect('/edit/ImageStore/?status=1&message=Image added/updated')
        

def DeleteImage(imageStringKey):
    image = dbImageStore.ImageStore.get(db.Key(imageStringKey))
    imageDescriptions = dbImageStore.ImageDescription.gql('WHERE imageEntry = :imageEntry', imageEntry = image.key()).fetch(10)
    
    db.delete(imageDescriptions)
    db.delete(image)
    
    return { 'status' : 1, 'message' : 'Image removed' }

def getById(imageId):
    imageMemcacheId = 'cached_image_' + str(imageId)
    imageEntry = memcache.get(imageMemcacheId)

    if imageEntry is None or Settings.forceMemcacheRefresh:
        imageEntry = dbImageStore.ImageStore.get_by_id(int(imageId))
        memcache.set(imageMemcacheId, imageEntry, Settings.memcacheTimeout)

    return imageEntry

def getByIdForEdit(imageId):
    imageEntry = dbImageStore.ImageStore.get_by_id(int(imageId))
    message = dict(imageEntry = None, imageDescription = None)
    if imageEntry:
        imageDescription = dbImageStore.ImageDescription.gql('WHERE imageEntry = :imageEntry', imageEntry = imageEntry.key())
        message = dict(imageEntry = imageEntry, imageDescription = imageDescription)
    return message

def getImageWithDescription(imageId, language):
    if not imageId or not language:
        return { 'url' : '', 'reference' : '', 'description' : '', 'itemId' : str(imageId) }

    image = getById(int(imageId))

    imageMemcacheId = 'cached_image_description_' + str(imageId) + '_' + language
    description = memcache.get(imageMemcacheId)
    if description is None or Settings.forceMemcacheRefresh:
        description = dbImageStore.ImageDescription.gql('WHERE imageEntry = :imageEntry AND lang = :lang', imageEntry = image.key(), lang = language).get()
        memcache.set(imageMemcacheId, description, Settings.memcacheTimeout)

    if description is None:
        descriptionText = ''
    else:
        descriptionText = description.description

    return { 'url' : image.imageUrl, 'reference' : image.imageReferance, 'description' : descriptionText, 'itemId' : str(imageId) }


def getImageListDescriptions(imageStringIdList, language):
    list = []
    imageList = imageStringIdList.split(',')
    for imageId in imageList:
        list.append(getImageWithDescription(imageId, language))
        
    return list

def getAll():
    try:
        images = db.GqlQuery('SELECT * FROM ImageStore').fetch(1000)
    except KindError:
        images = []

    return images