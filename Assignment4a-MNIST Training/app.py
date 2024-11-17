from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from train import TrainingManager
import threading

app = Flask(__name__)
socketio = SocketIO(app)
training_manager = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/start_training')
def start_training():
    global training_manager
    training_manager = TrainingManager(socketio)
    
    def train_thread():
        training_manager.train()
    
    thread = threading.Thread(target=train_thread)
    thread.start()
    return jsonify({'status': 'Training started'})

@app.route('/get_predictions')
def get_predictions():
    if training_manager is None:
        return jsonify({'error': 'Model not trained'})
    predictions = training_manager.get_random_predictions()
    return jsonify(predictions)

if __name__ == '__main__':
    socketio.run(app, debug=True) 