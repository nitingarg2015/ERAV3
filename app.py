from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Set up the folder where images are stored
# IMAGE_FOLDER = '\\static\\images'

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

    # # Construct the image path
    # image_path = os.path.join(app.config['IMAGE_FOLDER'], f"{animal_name}.jpg")
    # print(image_path)
    # # Check if the image exists
    # if not os.path.exists(image_path):
    #     return jsonify({'error': 'Image not found'}), 404

    # Return the image URL (relative to the server's root)
    return jsonify({'image_url': f"/static/images/{animal_name}.jpg"}), 200

if __name__ == '__main__':
    app.run(debug=True)
