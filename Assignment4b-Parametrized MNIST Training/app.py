from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from model import MnistCNN
import torch
import torch.optim as optim
from train import train_model

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
def train():
    try:
        # Get hyperparameters from form
        epochs = int(request.form['epochs'])
        batch_size = int(request.form['batch_size'])
        learning_rate = float(request.form['learning_rate'])
        optimizer_name = request.form['optimizer']
        
        # Get model channels
        channels = [1]  # Input channel is always 1 for MNIST
        for i in range(1, 4):
            channels.append(int(request.form[f'channel_{i}']))
        
        # Initialize model
        model = MnistCNN(layer_channels=channels)
        
        # Set optimizer
        if optimizer_name == 'adam':
            optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        else:
            optimizer = optim.SGD(model.parameters(), lr=learning_rate)
        
        # Train model with socket updates
        train_model(model, optimizer, epochs, batch_size, socketio)
        
        return jsonify({"status": "completed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, debug=True) 