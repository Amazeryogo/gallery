import os
from werkzeug.utils import secure_filename
from flask import *
import json

x = json.load(open("config.json"))


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','mp4'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = x['UPLOAD_FOLDER']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    image_names = os.listdir(UPLOAD_FOLDER)
    print(image_names)
    return render_template('index.html',images=image_names)
@app.route('/add', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new Photo</title>
    <h1>Upload new Photo</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/remove/<name>')
def remove_file(name):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], name))
    return redirect("/")

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

app.run(host=x['HOST'],port=x['PORT'])
