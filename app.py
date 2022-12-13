import os
from test import application
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
	return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
   
@application.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
 
        file = request.files['file']
 
        if 'file' not in request.files:
            return render_template('upload.html')
 
        if file.filename == '':
            return render_template('upload.html')
 
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'],  filename))
 
    return render_template('upload.html')



if __name__ == "__main__":
    application.run()