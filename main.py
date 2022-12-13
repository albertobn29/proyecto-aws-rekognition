# from flask import Flask, request, abort, Response, render_template, url_for
import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import time
import aws.functionality as funcs

UPLOAD_FOLDER = './static/img/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
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
            filename = str(time.time())+'_'+secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            funcs.main(filename)
            return render_template('index.html', img='img/'+filename)
    return render_template('index.html')


# Run the app
if __name__ == "__main__":
    app.debug = True
    app.run()  # Running on http://127.0.0.1:5000/
