from flask import render_template, request, session, send_from_directory, redirect,url_for
from test import application
import os
from werkzeug.utils import secure_filename
 
#*** Backend operation
 
# WSGI Application
# Defining upload folder path
UPLOAD_FOLDER = '/tugas/code/static/uploads/'
# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
 
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
# Configure upload folder for Flask application
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# Define secret key to enable session
 
 
@application.route('/in')
def im():
    return render_template('poto.html')
 
@application.route('/in',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(application.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(application.config['UPLOAD_FOLDER'], img_filename)
 
        return render_template('poto2.html')
 
@application.route('/show_image')
def displayImage():
    # Retrieving uploaded file path from session
    img_file_path = session.get('uploaded_img_file_path', None)
    # Display image in Flask application web page
    return render_template('show_image.html', user_image = img_file_path)
 
if __name__=='__main__':
    application.run(debug = True)