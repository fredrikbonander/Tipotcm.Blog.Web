__author__ = 'broken'

from google.appengine.api import mail

def send(senderName, senderEmail, body):
    mail.send_mail(sender = 'www.martinadlerphotography.com <gae@cloudnine.se>',
              to = 'images@martinadlerphotography.com',
              subject = 'From ' + senderName,
              body = 'Email: ' + senderEmail + '\n\n' + body)

    return { 'status' : 1, 'message' : 'Message sent' }