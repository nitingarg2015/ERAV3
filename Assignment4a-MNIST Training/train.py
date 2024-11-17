import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from model import MnistCNN
import json
from flask_socketio import SocketIO

class TrainingManager:
    def __init__(self, socketio):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = MnistCNN().to(self.device)
        self.socketio = socketio
        
        # Data loading
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        
        self.train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
        self.test_dataset = datasets.MNIST('./data', train=False, transform=transform)
        
        self.train_loader = DataLoader(self.train_dataset, batch_size=64, shuffle=True)
        self.test_loader = DataLoader(self.test_dataset, batch_size=64)
        
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        
    def train(self, epochs=10):
        for epoch in range(epochs):
            self.model.train()
            running_loss = 0.0
            
            for batch_idx, (data, target) in enumerate(self.train_loader):
                data, target = data.to(self.device), target.to(self.device)
                
                self.optimizer.zero_grad()
                output = self.model(data)
                loss = self.criterion(output, target)
                loss.backward()
                self.optimizer.step()
                
                running_loss += loss.item()
                
                if batch_idx % 100 == 0:
                    avg_loss = running_loss / (batch_idx + 1)
                    self.socketio.emit('training_update', {
                        'epoch': epoch + 1,
                        'batch': batch_idx,
                        'loss': avg_loss
                    })
            
            # Evaluate after each epoch
            test_accuracy = self.evaluate()
            self.socketio.emit('epoch_end', {
                'epoch': epoch + 1,
                'loss': running_loss / len(self.train_loader),
                'accuracy': test_accuracy
            })
    
    def evaluate(self):
        self.model.eval()
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in self.test_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                _, predicted = torch.max(output.data, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()
        
        return 100 * correct / total
    
    def get_random_predictions(self, num_samples=10):
        self.model.eval()
        indices = torch.randperm(len(self.test_dataset))[:num_samples]
        results = []
        
        with torch.no_grad():
            for idx in indices:
                image, label = self.test_dataset[idx]
                image = image.unsqueeze(0).to(self.device)
                output = self.model(image)
                pred = output.argmax(dim=1).item()
                results.append({
                    'image': image.cpu().numpy().squeeze().tolist(),
                    'prediction': pred,
                    'actual': label
                })
        
        return results 