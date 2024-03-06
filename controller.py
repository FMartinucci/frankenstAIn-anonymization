import random
import string
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
from csv_processor import CSVProcessor
from threading import Thread

import os

app = Flask(__name__)

UPLOAD_FOLDER= os.path.dirname(__file__) + "/data/input/"
RESULTS_FOLDER= os.path.dirname(__file__) +  '/data/results/'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def id_generator(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def start_process(filename: string, out_file: string):
    print('filename: ' + filename + ', out_file: ' + out_file)
    processor = CSVProcessor("spacy")
    processor.process_csv(filepath=filename, out_file=out_file)

@app.post('/anonymize_csv')
def upload_csv():
    if 'file' not in request.files:
        return {"error": "No file provided"}, 400
    file = request.files['file']

    if file.filename == '':
        return {"error": "No file provided"}, 400
    if file and allowed_file(file.filename):
        filename = UPLOAD_FOLDER + secure_filename(file.filename)
        file.save(filename)
        code = id_generator(size=5)
        out_file = RESULTS_FOLDER + 'output_' + code + '.csv'
        print('prima di asyncio')
        Thread(target=start_process, kwargs={'filename' : filename, 'out_file' : out_file}).start()
        return {"code": code}, 200
    else:
        return {"error": "Only .csv files"}, 400
    
@app.post('/result')
def get_result():
    if request.is_json:
        body = request.get_json()
        code = body["code"]
        filename = 'output_' + code + '.csv'
        return send_from_directory(app.config["RESULTS_FOLDER"], filename, as_attachment=True)
    return {"error": "Request must be JSON"}, 415
    

if __name__ == '__main__':
   app.run(debug = True, port=5001)