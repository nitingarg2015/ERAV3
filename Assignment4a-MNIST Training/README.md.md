# MNIST CNN Training Visualization

## Assignment
Create a flask api to train MNIST dataset using Cursor AI or ChatGPT

## Description

This project provides a web API that accepts handwritten digit images and returns predictions using a trained MNIST model. The API is built with Flask and uses a PyTorch model to classify digits from 0-9. It implements a 4-layer CNN for MNIST digit classification with real-time training visualization using Flask.

Demo Video: 

## Prompt used on Cursor AI
Write a simple 4 layer convolutional neural network, to be trained on MNIST. While the training is going on, i want to see the training logs and loss curves on an html page. use simple python flask server to do this. after training is done, show model. results on 10 random images picked from MNIST database. Use CUDE for training. write all the files including howTo.md file descibing the steps

## Model Summary
----------------------------------------------------------------
        Layer (type)               Output Shape         Param #
================================================================
            Conv2d-1           [-1, 32, 28, 28]             320
              ReLU-2           [-1, 32, 28, 28]               0
         MaxPool2d-3           [-1, 32, 14, 14]               0
            Conv2d-4           [-1, 64, 14, 14]          18,496
              ReLU-5           [-1, 64, 14, 14]               0
         MaxPool2d-6             [-1, 64, 7, 7]               0
            Conv2d-7            [-1, 128, 7, 7]          73,856
              ReLU-8            [-1, 128, 7, 7]               0
         MaxPool2d-9            [-1, 128, 3, 3]               0
           Conv2d-10            [-1, 256, 3, 3]         295,168
             ReLU-11            [-1, 256, 3, 3]               0
AdaptiveAvgPool2d-12            [-1, 256, 1, 1]               0
          Flatten-13                  [-1, 256]               0
           Linear-14                  [-1, 128]          32,896
             ReLU-15                  [-1, 128]               0
          Dropout-16                  [-1, 128]               0
           Linear-17                   [-1, 10]           1,290
================================================================
Total params: 422,026
Trainable params: 422,026
Non-trainable params: 0
----------------------------------------------------------------
Input size (MB): 0.00
Forward/backward pass size (MB): 0.79
Params size (MB): 1.61
Estimated Total Size (MB): 2.41
----------------------------------------------------------------

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









