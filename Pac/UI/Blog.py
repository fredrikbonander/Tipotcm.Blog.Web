__author__ = 'broken'

from google.appengine.ext import db
from Pac.DataFactory import dbBlogPosts
from Pac.DataFactory import dbPutQueue

def getByPageModuleKey(pageModuleKey):
    return dbBlogPosts.BlogPost.gql('WHERE pageModuleKey = :pageModuleKey ORDER BY date DESC', pageModuleKey = pageModuleKey).fetch(100)

def addNewBlogPost(pageModuleStringKey, language):
    blogPost = dbBlogPosts.BlogPost()
    blogPost.pageModuleKey = db.Key(pageModuleStringKey)
    blogPost.language = language

    return blogPost

def updateBlogPost(pageModuleStringKey, blogPostStringKey, language, title, content):
    if blogPostStringKey == '':
        blogPost = addNewBlogPost(pageModuleStringKey, language)
        message = 'Blog post added'
    else:
        blogPost = dbBlogPosts.BlogPost.get(db.Key(blogPostStringKey))
        message = 'Blog post updated'

    blogPost.title = title
    blogPost.content = content

    dbPutQueue.append(blogPost)

    return { 'status' : 1, 'message' : message }

def getPostById(blogPostId):
    return dbBlogPosts.BlogPost.get_by_id(int(blogPostId))


def getLatestBlogPost():
    return dbBlogPosts.BlogPost.all().order('-date').get()