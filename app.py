from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch the animal image
@app.route('/get-animal-image', methods=['GET'])
def get_animal_image():
    animal_name = request.args.get('animal')

    if not animal_name:
        return jsonify({'error': 'No animal specified'}), 400

    return jsonify({'image_url': f"/static/images/{animal_name}.jpg"}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        file_size = os.path.getsize(file_path)
        file_type = file.content_type
        
        return jsonify({
            'name': filename,
            'size': f"{file_size} bytes",
            'type': file_type
        })
    
if __name__ == '__main__':
    app.run(debug=True)
