from flask import Flask, request, jsonify
from process_image import process_image
from werkzeug.utils import secure_filename
import os
basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask('__name__')
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

_VERSION = 1 #version 1

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(400)
def page_empty_payload(error):
	response = jsonify({'message': 'payload cannot be empty'})
	return response, 400

@app.errorhandler(401)
def page_unauthorized(error):
	response = jsonify({'message': 'invalid authorization'})
	return response, 401

@app.errorhandler(404)
def page_not_found(error):
	response = jsonify({'message': 'page not found'})
	return response, 404

@app.errorhandler(500)
def internal_server_error(error):
	response = jsonify({'message': 'internal server error'})
	return response, 500

@app.route('/', methods=['GET'])
def index():
    return 'welcome'

@app.route('/api/health-check', methods=['GET'])
def healthCheck():
    result = jsonify({'message': 'Your application running properly'})
    return result

@app.route('/api/ocr/images/v1', methods=['POST'])
def ocr():
    files = request.files['file']
    if files and allowed_file(files.filename):
        filename = secure_filename(files.filename)
        files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        path="./uploads/{}".format(filename)
        rec_string = process_image(path=path)
        os.remove(path)
        return jsonify(rec_string)
    else:
        result = jsonify({'err': True, 'message': 'type file not allowed!', 'data':''})
        return result, 403

app.run(host='0.0.0.0', port=3000)