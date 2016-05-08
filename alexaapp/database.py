from alexaapp import *
from flask_sqlalchemy import SQLAlchemy
from .config import *

db = SQLAlchemy(app)

# import a db_session to query db from other modules
db_session = db.session
username = "raneff@gmail.com"
password = "testalexa123"
aud_file_path = '../assets/audio/'
confidence = "85"

from VoiceIt import *
myVoiceIt = VoiceIt("f2fd3e6a0b3549fd916a908b7eef2da8")

def auth_user(audio_file_name):
	# send the audio file to the server to check whether it is authenticated
	response = myVoiceIt.authentication(username, password, aud_file_path + audio_file_name, confidence)
	return response

def enroll_user(audio_file_name):
	# send enrollment audio to the user to auth the user
	response = myVoiceIt.createEnrollment(username, password, aud_file_path + audio_file_name)
	return response

