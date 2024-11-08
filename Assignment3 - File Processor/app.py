from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from mimetypes import guess_type
from typing import Any
from imports.textdataset import TextDataSet
from imports.imagedataset import ImageDataSet
from imports.audiodataset import AudioDataSet
from imports.threeDdataset import ThreeDDataset

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'

DATACLASS: Any = None # initialize to respective data type on upload of file based on filetype
FILETYPE: str = None

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg', 'gif', 'wav', 'mp3', 'off'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<path:filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def get_mime_type(filepath):
    mime_type, encoding = guess_type(filepath)
    if mime_type is None and filepath.lower().endswith('.off'):
        mime_type = 'model/off'  # Manually set MIME type for .off files
    return mime_type

@app.route('/upload', methods=['POST'])
def upload_file():
    global DATACLASS, FILETYPE  # Declare globals

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'No selected file or unsupported file type'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Return file metadata
        file_metadata = {
            'filename': filename,
            'size': os.path.getsize(filepath),
            'path': filepath,
            'type': get_mime_type(filepath)  # Get MIME type
        }

    # Check the file type and initialize dataclass based on file type
    mime_type = get_mime_type(filepath)
    print(f"mime_type is {mime_type}")

    if mime_type.startswith('text/'):
        DATACLASS = TextDataSet(file_path=filepath)
        FILETYPE = 'text'
    elif mime_type.startswith('image/'):
        DATACLASS = ImageDataSet(file_path=filepath)
        FILETYPE = "image"

    elif mime_type.startswith('audio/'):
        DATACLASS = AudioDataSet(file_path=filepath)
        FILETYPE = 'audio'
    
    # elif mime_type.startswith('model/'):
    #     DATACLASS = ThreeDDataset(file_path=filepath)
    #     FILETYPE = 'model'

    print("checking type in upload function",type(DATACLASS))
    print(f"Filetype when closing upload function is {FILETYPE}")
    return jsonify(file_metadata), 200

@app.route('/view_file', methods=['GET'])
def view_file():
    global DATACLASS, FILETYPE  # Declare globals

    if DATACLASS is not None:
        try:
            content = DATACLASS.contents
            return jsonify({'content': content, 'type': FILETYPE}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 400            
    else:
        return jsonify({'error': 'Unsupported file type'}), 400
    
@app.route('/preprocess_file', methods=['GET'])
def preprocess_file():
    global DATACLASS, FILETYPE  # Declare globals
    filename = request.args.get('filename')

    if DATACLASS is not None:
        try:
            content = DATACLASS.preprocess_all()
            return jsonify({'content': content, 'type': FILETYPE}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 400            
    else:
        return jsonify({'error': 'Unsupported file type'}), 400
    
@app.route('/augment_file', methods=['GET'])
def augment_file():
    global DATACLASS, FILETYPE  # Declare globals

    if DATACLASS is not None:
        try:
            content = DATACLASS.augment_all()
            return jsonify({'content': content, 'type': FILETYPE}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 400            
    else:
        return jsonify({'error': 'Unsupported file type'}), 400
        
if __name__ == '__main__':
    app.run(debug=True)
