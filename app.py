from flask import Flask, url_for, redirect, flash, request, render_template
from gingerit.gingerit import GingerIt
from werkzeug.utils import secure_filename
import os
from cv2 import cv2
import numpy as np
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
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
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    back = find_background(filepath)
    flash(back)
    txt = find_text(filepath)
    flash(txt)
    flash('Image successfully uploaded')
    if processed_text == text:
        flash("Description is correct: " + processed_text)
        return render_template('index.html', filename = filename)
    else:
        flash("Incorrect description: "+text)
        flash("The correct description is: " + processed_text)
        return render_template('index.html', filename = filename)


#find if text is present in an image or not.
def find_text(path):
    img = cv2.imread(path)
    text = pytesseract.image_to_string(img)
    if text:
        return "Text present: "+text+" , REJECT IMAGE"
    else:
        return "No text present, Image accepted"

#find the background color of the Image.
def find_background(path, thresh = 0.3):
    print(type(path))
    img_Arr = cv2.imread(path)
    bckground = np.array([255,255,255])
    perc = (img_Arr == bckground).sum()/img_Arr.size

    if perc>=thresh:
        print(perc)
        return "White Background, IMAGE ACCEPTED"
    else:
        return "Color Background, REJECT IMAGE"

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/'+filename), code = 301)




if __name__=="__main__":
    app.run(debug = True)