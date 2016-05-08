from alexaapp import *
from alexaapp.forms import *
from alexaapp.database import *
from alexaapp.models import *
from flask import flash
import flask.ext.login as flask_login
import string, random
import json

def randomword(length):
        '''generate a random string of whatever length, good for filenames'''
        return ''.join(random.choice(string.lowercase) for i in range(length))

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):				# used by Flask internally to load logged-in user from session
	return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():					# not logged-in callback
	return "Not authorized."

@app.route("/", methods=['GET'])
def index():
	return render_template("index.html")
	
@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('../assets', path)

@app.route("/upload", methods=['GET', 'POST'])
def add_audio():
	audio_dirname = '../assets/audio/'
	form = AudioFileForm(request.form)
	if request.method == 'POST' and form.validate():
		form.audio_file.data = request.files['audio_file']
		if form.audio_file.data:
			file_name = "test_" + randomword(32) + ".wav"
			form.audio_file.data.save(audio_dirname + file_name)
			flash('Audiofile added.')
		else:
			flash('Error: No audiofile uploaded.')
	return render_template("form.html", action="Add an audiofile", form=form)

@app.route("/enroll_user", methods=['GET', 'POST'])
def enroll_user_form():
	audio_dirname = '../assets/audio/'
	form = AudioFileForm(request.form)
	printphrase = "My voice is my secured password."
	response = None
	if request.method == 'POST' and form.validate():
		form.audio_file.data = request.files['audio_file']
		if form.audio_file.data:
			file_name = "test_" + randomword(32) + ".wav"
			form.audio_file.data.save(audio_dirname + file_name)
			response = enroll_user(file_name)
			flash('Enrolled you in the database.')
		else:
			flash('Error: You did not upload an audio file.')
	return render_template("enroll_form.html", action="Enroll in AlexaDisrupt", form=form, phrase=printphrase, response=response)

@app.route("/auth_user", methods=['GET', 'POST'])
@login_manager.unauthorized_handler
def auth_user_form():
	audio_dirname = '../assets/audio/'
	form = AudioFileForm(request.form)
	printphrase = "My voice is my secured password."
	response = None
	if request.method == 'POST' and form.validate():
		form.audio_file.data = request.files['audio_file']
		if form.audio_file.data:
			file_name = "test_" + randomword(32) + ".wav"
			form.audio_file.data.save(audio_dirname + file_name)
			response = auth_user(file_name)

			flash('Checked authentication.')
		else:
			flash('Error: You did not upload an audio file.')
	return render_template("enroll_form.html", action="Authenticate with AlexaDisrupt", form=form, phrase=printphrase, response=response)

@app.route("/logged_in", methods=["GET", "POST"])
@flask_login.login_required
def logged_in_check():
	return "Logged in."

@app.route("/init", methods=["GET", "POST"])
def init_session():
	user = User.query.get("raneff@gmail.com") 
	user.session_token = "none"
	user.authenticated = False
	db_session.add(user)
	db_session.commit()
	return Response(response=json.dumps({"init":"success"}),
                    status=200,
                    mimetype="application/json")

@app.route("/status", methods=["GET", "POST"])
def status_session():
	status = False
	user = User.query.get("raneff@gmail.com") 
	if user.session_token != "none":
		if user.authenticated == False:
			status = True
	return Response(response=json.dumps({"status":status}),
                    status=200,
                    mimetype="application/json")

@app.route("/authenticate_audio", methods=["GET", "POST"])
def authenticate_audio():
	status = False
	user = User.query.get("raneff@gmail.com") 
	if user.session_token != "none":
		if user.authenticated == False:
			status = True
	if status == True:
		if request.method == 'POST' and form.validate():
			form.audio_file.data = request.files['audio_file']
			if form.audio_file.data:
				file_name = "test_" + randomword(32) + ".wav"
				form.audio_file.data.save(audio_dirname + file_name)
				response = auth_user(file_name)
				if response["ResponseCode"] == "SUC":
					status = "authenticated"
				else:
					status = "retry"
			else:
				status = "no audio sent"
		else:
			status = "need to post multipart form data"
	else:
		status = "not ready"
	return Response(response=json.dumps({"verify":status}),
                    status=200,
                    mimetype="application/json")

@app.route("/hello_world", methods=["GET", "POST"])
def hello_world():
	''' 
		{
		 "session": {
		   "sessionId": "SessionId.1b7602de-efef-4032-a5a0-4357e73e6210",
		   "application": {
		     "applicationId": "amzn1.echo-sdk-ams.app.5bd23eb7-5e5e-4641-a7d2-abf9303fe8a6"
		   },
		   "user": {
		     "userId": "amzn1.ask.account.AFP3ZWPOS2BGJR7OWJZ3DHPKMOMNWY4AY66FUR7ILBWANIHQN73QHVCH7FRY4MCKNIO4EGHXMAS7WFK4JQHKXTQPRQ6NYR3N7YBZT7D25NJXYI7H6TERSQYEPE57OE6MIYWTBI5CBJLZFBFC2BC4245KCPS7H753EEXDYYKCRAUZX32S4XXFTYQISZAZX2N2LJ4HN4RVEG6VQLI"
		   },
		   "new": true
		 },
		 "request": {
		   "type": "IntentRequest",
		   "requestId": "EdwRequestId.f21c7d51-ceb3-4164-aeb8-39618fb28155",
		   "timestamp": "2016-05-08T04:45:10Z",
		   "intent": {
		     "name": "PayPerson",
		     "slots": {
		       "Amount": {
		         "name": "Amount",
		         "value": "20"
		       },
		       "Person": {
		         "name": "Person",
		         "value": "Chris"
		       }
		     }
		   },
		   "locale": "en-US"
		 },
		 "version": "1.0"
		}
	'''
	content = request.get_json(silent=True)

	user = User.query.get("raneff@gmail.com") 
	user.session_token = content["session"]["sessionId"] if content else None
	db_session.add(user)
	db_session.commit()

	# canned response
	response = respond_alexa("Welcome to the Alexa Disrupt app, you can say hello")
	if content:
		if "intent" in content["request"].keys():
			if content["request"]["intent"]["name"] == "PayPerson":
				response = respond_alexa(pay_person(content))

	#respond
	resp = Response(response=json.dumps(response),
                    status=200,
                    mimetype="application/json")
	return resp

def pay_person(content):
	user = User.query.get("raneff@gmail.com")
	response = None
	person_name = None
	try:
		person_name = content["request"]["intent"]["slots"]["Person"]["value"]
	except:
		response = "Sorry, I didn't catch who you wanted to pay "

	try:
		pay_amount = content["request"]["intent"]["slots"]["Amount"]["value"]
	except:
		if response != None:
			response +="and the amount to pay them."
		else:
			response = "Sorry, I didn't catch how much you wanted to pay."

	#okay, we have a response and the amount
	if response == None:
		if user.is_authenticated == 1:
			response = "Okay, I will pay " + person_name + " " + pay_amount + " dollars via your Venmo balance."
		else:
			response = "Say your passphrase to pay " + person_name + " " + pay_amount + '.'
	return response



def respond_alexa(response_text):
	''' example output
	{ "version": "1.0",
	  "response": {
	    "outputSpeech": {
	      "type": "PlainText",
	      "text": "Welcome to the Alexa Skills Kit, you can say hello"
	    },
	    "card": {
	      "type": "Simple",
	      "title": "HelloWorld",
	      "content": "Welcome to the Alexa Skills Kit, you can say hello"
	    },
	    "reprompt": {
	      "outputSpeech": {
	        "type": "PlainText",
	        "text": "Welcome to the Alexa Skills Kit, you can say hello"
	      }
	    },
	    "shouldEndSession": false
	  },
	  "sessionAttributes": {}
	}
	'''
	response = {}
	response["version"] = "1.0"
	response["shouldEndSession"] = False
	response2 = {}
	response2["outputSpeech"] = {"type": "PlainText",
	      "text": response_text}
	response2["card"] = {
	      "type": "Simple",
	      "title": "HelloDisrupt",
	      "content": response_text
	    }
	response2["reprompt"] = {"outputSpeech" : response2["outputSpeech"]}
	response["response"] = response2
	response["sessionAttributes"] = {}
	return response

