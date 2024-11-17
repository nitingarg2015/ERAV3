import torch
import torch.nn as nn

class MnistCNN(nn.Module):
    def __init__(self, layer_channels=None):
        super(MnistCNN, self).__init__()
        
        if layer_channels is None:
            layer_channels = [1, 32, 64, 128]  # default values
        
        self.conv_layers = nn.Sequential(
            nn.Conv2d(layer_channels[0], layer_channels[1], kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Conv2d(layer_channels[1], layer_channels[2], kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Conv2d(layer_channels[2], layer_channels[3], kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        
        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(layer_channels[3] * 3 * 3, 10)
        )
        
    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x 