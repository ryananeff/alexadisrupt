from alexaapp import *
from alexaapp.forms import *
from flask import flash

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
			form.audio_file.data.save(audio_dirname + request.form['audio_file_name'])
			flash('Audiofile added.')
		else:
			flash('Error: No audiofile uploaded.')
	return render_template("form.html", action="Add an audiofile", form=form)
