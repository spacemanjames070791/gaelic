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
	question = ndb.StringProperty()
	option1 = ndb.StringProperty()
	option2 = ndb.StringProperty()
	option3 = ndb.StringProperty()
	option4 = ndb.StringProperty()
	answer = ndb.StringProperty()

	def toJSON(self):
		jsonquestion = {
			"question": self.question,
			"option1": self.opt1,
			"option2": self.opt2,
			"option3": self.opt3,
			"option4": self.opt4,
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


class MainHandler(webapp2.RequestHandler):
	def get(self):

app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/translateWord/(.*)', TranslateWord),
	('/questions', QuestionHandler),
	('/register', NewUser),
	('/login/(.*)/(.*)', Login),
	('/location/(.*)', Location)
], debug=True)
