from app import app
from flask import render_template, request, redirect, flash, url_for, send_from_directory, jsonify
from config import ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
from app import models, db
import os, datetime


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    query = models.Image.query.paginate(page, 3, False)
    return render_template('index.html', images=query)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # add file info to the database
            img = models.Image(filename=filename, created_date=datetime.datetime.utcnow())
            db.session.add(img)
            db.session.commit()

            return redirect(url_for('index'))
    else:
        return render_template('upload.html')


@app.route('/image/<filename>')
def return_pic(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/getpage', methods=['POST'])
def get_page():
    page = int(request.form.get('pageNumber', 0))
    size = int(request.form.get('pageSize', 0))
    query = models.Image.query.paginate(page, 3, False)
    data = [
        {'url': url_for('return_pic', filename=img.filename),
         'filename': img.filename,
         'date': img.created_date} for img in query.items]

    return jsonify(data)
