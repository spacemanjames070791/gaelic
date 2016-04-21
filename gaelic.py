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
from webapp2_extras import sessions

import logging

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
	name = ndb.StringProperty(required=True)
	password = ndb.StringProperty()

	def toJSON(self):
		jsonuser = {
			"email" : self.key.id(),
			"name": self.name,
			"password": self.name,
		}
		return json.encode(jsonuser)

class NewUser(webapp2.RequestHandler):
	def get(self):
		email = self.request.get('email')
		name = self.request.get('name')
		password = self.request.get('password')
		callback = self.request.get('callback')
		usr = User(id=email)
		usr.name = name
		usr.password = password
		usr.put()

class Login(webapp2.RequestHandler):
	def get(self):
		cust = User.get_by_id(self.request.get('name'))
		callback = (self.request.get('callback'))

		p=""
		username=self.request.get('name')
		user = User.query()
		user = user.filter(User.name==username)
		for usr in user:
			p+=usr.toJSON()

		p = p[:-1]

		response = callback + '({"user":"'+cust.key.id()+\
				   '","credentials":[{"name":"' + str(cust.name) + '","password":"' + str(cust.password) + '"}]})'

		self.response.write(response)

class LoadQuestions(webapp2.RequestHandler):

	def get(self):
		msg = Question()
		msg.user = 'neil@bedrock.com'
		msg.message = 'What is the word for cold?'
		msg.opt1 = 'fuar'
		msg.opt2 = 'blah'
		msg.opt3 = 'fliuch'
		msg.opt4 = 'tioram'
		msg.answer = 'fuar'
		msg.put()

		msg = Question()
		msg.user = 'neil@bedrock.com'
		msg.message = 'What is the word for Butter?'
		msg.opt1 = 'an t-aran'
		msg.opt2 = 'an t-im'
		msg.opt3 = 'an t-uisge'
		msg.opt4 = 'am bainne'
		msg.answer = 'an t-im'
		msg.put()

		msg = Question()
		msg.user = 'neil@bedrock.com'
		msg.message = 'What is the correct grammar for "I am going to be happy"'
		msg.opt1 = 'Bi toilichte!'
		msg.opt2 = 'Bidh thu toilichte.'
		msg.opt3 = 'Bithibh toilichte!'
		msg.opt4 = 'Tha mi gu bhith toilichte'
		msg.answer = 'Tha mi gu bhith toilichte'
		msg.put()
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
		# Now build a response of JSON messages..
		for wd in words:
			jsonresponse += wd.toJSON() + ','
		# and add in the callback function if required...
		if(callback == ''):
			self.response.write('[' + jsonresponse[:-1] + ']')
		else:
			self.response.write(callback + '([' + jsonresponse[:-1] + ']);')

class LoadWord(webapp2.RequestHandler):

	def get(self):
		word = Word()
		word.englishWord = 'Hello'
		word.gaelicWord = 'Halo'
		word.pronunciation = 'pronounce'
		word.plural = 'plural'
		word.put()
		self.response.write("OK")

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("home page")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/load', LoadQuestions),
	('/loadword', LoadWord),
	('/translateWord/(.*)', TranslateWord),
    ('/users/(.*)', QuestionHandler)
], debug=True)