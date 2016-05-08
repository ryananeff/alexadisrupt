from alexaapp import *
from wtforms import Form, TextField, validators, FileField

class AudioFileForm(Form):
	audio_file = FileField('Upload new audio')
