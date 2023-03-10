import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import time
import aws.functionality as funcs
from dotenv import load_dotenv
load_dotenv()

UPLOAD_FOLDER = './static/img/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', err='No hay archivo')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', err='Archivo incorrecto')
        if file and allowed_file(file.filename):
            funcs.checkBuckets()
            filename = str(time.time())+'_'+secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = funcs.main(filename)
            return render_template('index.html', data=data)
        else:
            return render_template('index.html', err='Extension de la imagen incorrecta')
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


# Run the app
if __name__ == "__main__":
    app.debug = True
    app.run()  # Running on http://127.0.0.1:5000/
