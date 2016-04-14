import webapp2
from google.appengine.ext import ndb
from webapp2_extras import json
import logging

instructionsPage = """
<html><head><title>auws-msgboard Demo App</title></head>
<body>
	<h1>auws-msgboard Demo App</h1>
	<p>This app is a simple demonstration client-server app for mobile devices.</p>
	<p>The app uses...</p>
	<ul>
		<li>Google App Engine for a server</li>
		<li>HTML5+Javascritp+CSS for the client</li>
		<li>jQuery and jQuery Mobile as the client framework</li>
		<li>JSON/JSONP as the app protocol</li>
	</ul>
	<p>The Google App Engine server is set up as a REST server, althugh there is only
	one resource URL defined.  Browsing to http://&lt;app domain&gt;/users/&lt;user-id&gt; will
	return the last 6 messages from the specified user.  The URL http://&lt;app domain&gt;/users/ 
	will return messages from ANY users.</p>
	<p>Posting a message to http://&lt;app domain&gt;/users/&lt;user-id&gt; will add a message 
	to the server's database.</p>

	<a href="html/index.html">Go to app main page</a>
</body>
"""

class Word(ndb.Model):
  englishWord = ndb.StringProperty()
  gaelicWord = ndb.StringProperty()
  pronunciation = ndb.StringProperty()
  plural = ndb.StringProperty()
  
  def toString(self):
    return self.englishWord + ':' + self.gaelicWord)
    
  def toJSON(self):
    jsonWord = {
      "englishWord": self.englishWord,
      "gaelicWord": self.gaelicWord
      }
      return json.encode(jsonWord)
      
class TestWord(webapp2.RequestHandler):

  def get(self):
    eWord = Word()
    eWord.englishWord = 'Hello'
    eWord.gaelicWord = 'halò'
    eWord.put()
      
class WordHandler(webapp2.RequestHandler):

  def get(self, englishWord):
    logging.info("englishWord=" + englishWord)
    logging.info(bool(englishWord != ""))
    if englishWord != "":
      self.response.write('Please enter a word!')
    jsonresponse = ''
    
    callback = self.request.get('callback')
    for gaelicWord in words:
      jsonresponse += gaelicWord.toJSON()
    if(callback == ''):
      self.response.write('[' + jsonresponse[:-1] + ']')
    else:
      self.response.write(callback + '([' + jsonresponse[:-1] + ']);')
      
  def post(self, englishWord):
    eWord = Word()
    eWord.englishWord = englishWord
    eWord.gaelicWord = self.request.get('gaelicWord')
    eWord.put()
    self.response.write(eWord.toJSON())
    
class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.response.write(instructionsPage)
    
app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/test', TestWord),
  ('/users/(.*)', WordHandler)
], debug=True)
