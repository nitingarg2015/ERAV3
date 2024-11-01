from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Set up the folder where images are stored and uploads are made
# IMAGE_FOLDER = '\\static\\images'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure the app to serve static files from the 'images' folder
# app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

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


if __name__ == '__main__':
    app.run(debug=True)
