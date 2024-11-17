import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import time

def train_model(model, optimizer, epochs, batch_size, socketio):
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    # Loss function
    criterion = nn.CrossEntropyLoss()
    
    # Data loading
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST('./data', train=False, transform=transform)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    # Training loop
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
            
            # Emit progress every 100 batches
            if batch_idx % 100 == 0:
                progress = {
                    'epoch': epoch + 1,
                    'batch': batch_idx,
                    'total_batches': len(train_loader),
                    'loss': running_loss / (batch_idx + 1),
                    'accuracy': 100. * correct / total
                }
                socketio.emit('training_update', progress)
        
        # Validation phase
        model.eval()
        test_loss = 0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                test_loss += criterion(output, target).item()
                _, predicted = output.max(1)
                total += target.size(0)
                correct += predicted.eq(target).sum().item()
        
        test_loss /= len(test_loader)
        test_accuracy = 100. * correct / total
        
        # Emit epoch results
        epoch_results = {
            'epoch': epoch + 1,
            'train_loss': running_loss / len(train_loader),
            'test_loss': test_loss,
            'test_accuracy': test_accuracy
        }
        socketio.emit('epoch_complete', epoch_results)
        
        # Small delay to prevent overwhelming the socket
        time.sleep(0.1)
    
    return {"status": "completed"}