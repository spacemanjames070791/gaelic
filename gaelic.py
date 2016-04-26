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
	<h1>Gaelic Translation Services</h1>

	<a href="html/index.html">Go to app main page</a>
</body>
"""

class Word(ndb.Model):
	englishWord = ndb.StringProperty()
	gaelicWord = ndb.StringProperty()
	pronunciation = ndb.StringProperty()
	plural = ndb.StringProperty()
	timestamp = ndb.DateTimeProperty(auto_now_add=True)

	def toString(self):
		return self.englishWord + ':' + self.gaelicWord + ':' + self.timestamp.strftime("%A %d/%m/%Y %H:%M")

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
	user = ndb.StringProperty()
	message = ndb.StringProperty()
	opt1 = ndb.StringProperty()
	opt2 = ndb.StringProperty()
	opt3 = ndb.StringProperty()
	opt4 = ndb.StringProperty()
	answer = ndb.StringProperty()
	timestamp = ndb.DateTimeProperty(auto_now_add=True)

	def toString(self):
		return self.user + ':' + self.message + ':' + self.timestamp.strftime("%A %d/%m/%Y %H:%M")

	def toJSON(self):
		jsonquestion = {
			"user": self.user,
			"message": self.message,
			"opt1": self.opt1,
			"opt2": self.opt2,
			"opt3": self.opt3,
			"opt4": self.opt4,
			"answer": self.answer
		}
		return json.encode(jsonquestion)

class User(ndb.Model):
	useremail = ndb.StringProperty(required = True)
	username = ndb.StringProperty(required=True)
	password = ndb.StringProperty()
	isOnline = ndb.BooleanProperty()

	def toJSON(self):
		jsonuser = {
			"useremail" : self.useremail,
			"username": self.username,
			"password": self.password,
			"isOnline": self.isOnline
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
	def get(self):
		email = self.request.get('email')
		username = self.request.get('username')
		password = self.request.get('password')
		callback = self.request.get('callback')
		usr = User(id=email)
		usr.useremail = email
		usr.username = username
		usr.password = password
		usr.isOnline = False
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

class LoadQuestions(webapp2.RequestHandler):

	def get(self):
		useremail = 'neil@mars.com'
		user = User(id=useremail)
		user.useremail = useremail
		user.username = 'Neil'
		user.password = 'nimbus'
		user.isOnline = False
		user.put()

		useremail = 'jamie@spacestation.com'
		user = User(id=useremail)
		user.useremail = useremail
		user.username = 'Jamie'
		user.password = 'crazyfrog'
		user.isOnline = False
		user.put()

		question = 'What is the word for cold?'
		msg = Question(id=question)
		msg.user = 'neil@bedrock.com'
		msg.message = 'What is the word for cold?'
		msg.opt1 = 'fuar'
		msg.opt2 = 'blah'
		msg.opt3 = 'fliuch'
		msg.opt4 = 'tioram'
		msg.answer = 'fuar'
		msg.put()

		question = 'What is the word for Butter?'
		msg = Question(id=question)
		msg.user = 'neil@bedrock.com'
		msg.message = 'What is the word for Butter?'
		msg.opt1 = 'an t-aran'
		msg.opt2 = 'an t-im'
		msg.opt3 = 'an t-uisge'
		msg.opt4 = 'am bainne'
		msg.answer = 'an t-im'
		msg.put()

		question = 'What is the correct grammar for "I am going to be happy"?'
		msg = Question(id=question)
		msg.user = 'neil@bedrock.com'
		msg.message = 'What is the correct grammar for "I am going to be happy"'
		msg.opt1 = 'Bi toilichte!'
		msg.opt2 = 'Bidh thu toilichte.'
		msg.opt3 = 'Bithibh toilichte!'
		msg.opt4 = 'Tha mi gu bhith toilichte'
		msg.answer = 'Tha mi gu bhith toilichte'
		msg.put()

		englishWord = 'Hello'
		word = Word(id=englishWord)
		word.englishWord = 'Hello'
		word.gaelicWord = 'Halo'
		word.pronunciation = 'pronounce'
		word.plural = 'plural'
		word.put()

		englishWord = 'Welcome'
		word = Word(id=englishWord)
		word.englishWord = 'Welcome'
		word.gaelicWord = 'Faite'
		word.pronunciation = 'pronounce'
		word.plural = 'plural'
		word.put()

		townName = 'Glasgow'
		town = Town(id=townName)
		town.townName = townName
		town.gaelic = 'Ghlaschu'
		town.put()

		self.response.write("OK")

class QuestionHandler(webapp2.RequestHandler):

	def get(self, user):
		# Note - depending on the URL, we should return messages from .
		# only a specified user or any user.
		# We'd rather get the last 6 messages from any users...
		logging.info("USER=" + user)
		logging.info(bool(user != ""))
		if user != "":
			questions = Question.query(Question.user == user).order(-Question.timestamp).fetch(5)
		else:
			questions = Question.query().order(-Question.timestamp).fetch(5)
		jsonresponse = ''
		callback = self.request.get('callback')
		# Now build a response of JSON messages..
		for question in questions:
			jsonresponse += question.toJSON() + ','
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


class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write(link)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/load', LoadQuestions),
	('/translateWord/(.*)', TranslateWord),
	('/users/(.*)', QuestionHandler),
	('/register', NewUser),
	('/login/(.*)/(.*)', Login),
	('/location/(.*)', Location)
], debug=True)
