# - *- coding: utf- 8 -*-
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
from google.appengine.ext import ndb
from webapp2_extras import json
import codecs

import logging

link = """
<html><head><title>Gaelic App</title></head>
<body>
	<h1>Loading, please wait...</h1>

	<meta HTTP-EQUIV="REFRESH" content="0; url=http://gaelic-1281.appspot.com/html/index.html">

</body>
"""

class Word(ndb.Model):
	englishWord = ndb.StringProperty()
	gaelicWord = ndb.StringProperty()
	pronunciation = ndb.StringProperty()
	plural = ndb.StringProperty()
	timestamp = ndb.DateTimeProperty(auto_now_add=True)

	def toString(self):
		return self.englishWord + ':' + self.gaelicWord + ':'

	def toJSON(self):
		jsonword = {
			"wordID" : self.key.id(),
			"englishWord": self.englishWord,
			"gaelicWord": self.gaelicWord,
			"pronunciation": self.pronunciation,
			"plural": self.plural
		}
		return json.encode(jsonword)

class Question(ndb.Model):
	question = ndb.StringProperty()
	option1 = ndb.StringProperty()
	option2 = ndb.StringProperty()
	option3 = ndb.StringProperty()
	option4 = ndb.StringProperty()
	answer = ndb.StringProperty()

	def toJSON(self):
		jsonquestion = {
			"question": self.question,
			"option1": self.option1,
			"option2": self.option2,
			"option3": self.option3,
			"option4": self.option4,
			"answer": self.answer
		}
		return json.encode(jsonquestion)

class User(ndb.Model):
	useremail = ndb.StringProperty(required = True)
	username = ndb.StringProperty(required=True)
	password = ndb.StringProperty()

	def toJSON(self):
		jsonuser = {
			"useremail" : self.useremail,
			"username": self.username,
			"password": self.password,
		}
		return json.encode(jsonuser)

class Town(ndb.Model):
	townName = ndb.StringProperty(required = True)
	gaelic = ndb.StringProperty(required=True)

	def toJSON(self):
		jsontown = {
			"townName" : self.townName,
			"gaelic": self.gaelic
		}
		return json.encode(jsontown)

class NewUser(webapp2.RequestHandler):
	def post(self):
		email = self.request.get('email')
		username = self.request.get('username')
		password = self.request.get('password')
		callback = self.request.get('callback')
		usr = User(id=email)
		usr.useremail = email
		usr.username = username
		usr.password = password
		usr.put()
		self.response.write("User added")

class Login(webapp2.RequestHandler):
	def get(self, email, password):
		jsonresponse = ''
		callback = self.request.get('callback')
		users = User.query()
		users = users.filter(User.useremail==email)
		# Now build a response of JSON messages..
		for usr in users:
			jsonresponse += usr.toJSON() + ','
		#ßand add in the callback function if required...
		if(callback == ''):
			self.response.write('[' + jsonresponse[:-1] + ']')
		else:
			self.response.write(callback + '([' + jsonresponse[:-1] + ']);')

class Location(webapp2.RequestHandler):
	def get(self, townName):
		jsonresponse = ''
		callback = self.request.get('callback')
		town = Town.query()
		town = town.filter(Town.townName==townName)
		# Now build a response of JSON messages..
		for tn in town:
			jsonresponse += tn.toJSON() + ','
		#ßand add in the callback function if required...
		if(callback == ''):
			self.response.write('[' + jsonresponse[:-1] + ']')
		else:
			self.response.write(callback + '([' + jsonresponse[:-1] + ']);')

class QuestionHandler(webapp2.RequestHandler):

	def get(self):
		questions = Question.query()
		jsonresponse = ''
		callback = self.request.get('callback')
		# Now build a response of JSON messages..
		for qstn in questions:
			jsonresponse += qstn.toJSON() + ','
		# and add in the callback function if required...
		if(callback == ''):
			self.response.write('[' + jsonresponse[:-1] + ']')
		else:
			self.response.write(callback + '([' + jsonresponse[:-1] + ']);')

class TranslateWord(webapp2.RequestHandler):

	def get(self, englishWord):
		jsonresponse = ''
		callback = self.request.get('callback')
		words = Word.query()
		words = words.filter(Word.englishWord==englishWord)
		# Now build a response of JSON messages..
		for wd in words:
			jsonresponse += wd.toJSON() + ','
		# and add in the callback function if required...
		if(callback == ''):
			self.response.write('[' + jsonresponse[:-1] + ']')
		else:
			self.response.write(callback + '([' + jsonresponse[:-1] + ']);')

class TestHandler(webapp2.RequestHandler):
	def get(self):
		useremail = 'neil@mars.com'
		user = User(id=useremail)
		user.useremail = useremail
		user.username = 'Neil'
		user.password = 'nimbus'
		user.put()

		useremail = 'jamie@spacestation.com'
		user = User(id=useremail)
		user.useremail = useremail
		user.username = 'Jamie'
		user.password = 'crazyfrog'
		user.put()

		question = "How do you say 'I don't understand?'"
		qst = Question(id=question)
		qst.question = question
		qst.option1 = "Chan eil mi 'tuigsinn"
		qst.option2 = "Chan eil a 'tuigsinn"
		qst.option3 = "Chan eil 'tuigsinn"
		qst.option4 = "Chan eil mi a 'tuigsinn"
		qst.answer = "Chan eil mi a 'tuigsinn"
		qst.put()

		question = "How many different forms of the definite article are there in Scots Gaelic?"
		qst = Question(id=question)
		qst.question = question
		qst.option1 = "8"
		qst.option2 = "1"
		qst.option3 = "4"
		qst.option4 = "6"
		qst.answer = "8"
		qst.put()

		question = "Which definite article is used in front of masculine words beginning with the consonants 'b,f,m and p'?"
		qst = Question(id=question)
		qst.question = question
		qst.option1 = "a'"
		qst.option2 = "an"
		qst.option3 = "na"
		qst.option4 = "am"
		qst.answer = "am"
		qst.put()

		question = "When should the definite article 'an' be used?"
		qst = Question(id=question)
		qst.question = question
		qst.option1 = "Before masculine words beginning with a vowel"
		qst.option2 = "Before feminine words beginning with a vowel	"
		qst.option3 = "Before feminine words beginning with a constenant"
		qst.option4 = "Before masculine words beginning with a constenant"
		qst.answer = "Before feminine words beginning with a vowel"
		qst.put()

		englishWord = 'hello'
		word = Word(id=englishWord)
		word.englishWord = englishWord
		word.gaelicWord = 'Halo'
		word.pronunciation = 'pronounce'
		word.put()

		englishWord = 'welcome'
		word = Word(id=englishWord)
		word.englishWord = englishWord
		word.gaelicWord = 'Faite'
		word.pronunciation = 'Fah-ti'
		word.put()

		townName = 'Glasgow'
		town = Town(id=townName)
		town.townName = townName
		town.gaelic = 'Ghlaschu'
		town.put()


		townName = 'Paisley'
		town = Town(id=townName)
		town.townName = townName
		town.gaelic = 'Phaslig'
		town.put()

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write(link)

app = webapp2.WSGIApplication([
	('/', MainHandler),
    ('/fill', TestHandler),
	('/translateWord/(.*)', TranslateWord),
	('/questions', QuestionHandler),
	('/register', NewUser),
	('/login/(.*)/(.*)', Login),
	('/location/(.*)', Location)
], debug=True)
