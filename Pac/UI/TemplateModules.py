__author__ = 'broken'

from Pac.DataFactory import dbImageStore
from Pac import ImageStore

def getStandardHeading(template, name):
    templateData = {}
    for lang in template.pageData:
        if name in template.pageData[lang]:
            templateData[lang] = template.pageData[lang][name]

    return { 'name' : name, 'type' : 'static', 'file' : 'modules/module_heading.html', 'data' : templateData }

def getStandardTextBox(template, name):
    templateData = {}
    for lang in template.pageData:
        if name in template.pageData[lang]:
            templateData[lang] = template.pageData[lang][name]

    return { 'name' : name, 'type' : 'static', 'file' : 'modules/module_textbox.html', 'data' : templateData }

def getSingleImageModule(template, name):
    templateData = {}
    imageList = dbImageStore.ImageStore.all()
    for lang in template.pageData:
        if name in template.pageData[lang] and template.pageData[lang][name] != '':
            templateData[lang] = ImageStore.getByIdForEdit(template.pageData[lang][name])['imageEntry']

    return { 'name' : name, 'type' : 'singleImage', 'file' : 'modules/module_page_single_image.html', 'data' : templateData, 'imageList' : imageList }

def getMultipleImagesModule(template, name):
    templateData = {}
    imageList = dbImageStore.ImageStore.all()
    for lang in template.pageData:
        if name in template.pageData[lang]:
            imageStringIdList = template.pageData[lang][name]
            templateData[lang] = { 'imageStringIdList' : imageStringIdList, 'imageCount' : str(len(imageStringIdList.split(','))) }

    return { 'name' : name, 'type' : 'multipleImage', 'file' : 'modules/module_select_multi_image.html', 'data' : templateData, 'imageList' : imageList }
