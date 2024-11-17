# MNIST CNN Training Visualization

## Assignment
Create a flask api to train MNIST dataset using Cursor AI or ChatGPT

## Description

This project provides a web API that accepts handwritten digit images and returns predictions using a trained MNIST model. The API is built with Flask and uses a PyTorch model to classify digits from 0-9. It implements a 4-layer CNN for MNIST digit classification with real-time training visualization using Flask.

Demo Video: 

## Prompt used on Cursor AI
Write a simple 4 layer convolutional neural network, to be trained on MNIST. While the training is going on, i want to see the training logs and loss curves on an html page. use simple python flask server to do this. after training is done, show model. results on 10 random images picked from MNIST database. Use CUDE for training. write all the files including howTo.md file descibing the steps

## Model Summary

![image](https://github.com/user-attachments/assets/0bebf035-b424-4b42-b5c3-f6d60592efd0)


## Prerequisites

- Python 3.7+
- Flask
- PyTorch (or TensorFlow, depending on your implementation)
- Pillow (PIL)
- NumPy

## Installation

1. Clone the repository
2. Install the dependencies
3. Run the API

## Usage
1. Start the Flask server
2. The API will be available at `http://localhost:5000`

### API Endpoints

#### POST /predict
Accepts an image file and returns the predicted digit.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: image file (PNG/JPEG format)









