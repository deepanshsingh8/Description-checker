from flask import Flask, url_for, redirect, flash, request, render_template
from gingerit.gingerit import GingerIt
from werkzeug.utils import secure_filename
import os
from autocorrect import Speller



UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.secret_key = "provenioai-catch"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def process(text):
    parser = GingerIt()
    output = parser.parse(text)
    return output.get("result")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['description']
    processed_text = process(text)
    if 'file' not in request.files:
        flash("No file part")
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    flash('Image successfully uploaded')
    if processed_text == text:
        flash("Description is correct: " + processed_text)
        return render_template('index.html', filename = filename)
    else:
        flash("Incorrect description: "+text)
        flash("The correct description is: " + processed_text)
        return render_template('index.html', filename = filename)



@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/'+filename), code = 301)




if __name__=="__main__":
    app.run(debug = True)