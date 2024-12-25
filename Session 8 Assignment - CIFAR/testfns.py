from tqdm import tqdm
import torch


def test(model, device, test_loader):
    '''
    test function taken inputs as pre defined model, device, test_loader (dataloader)
    It returns the following: test loss, test accuracy for that epoch
    '''
    criterion = torch.nn.CrossEntropyLoss()
    
    model.eval()
    loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)

            loss += criterion(output, target).item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)\n'.format(
        loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

    acc = 100. * correct / len(test_loader.dataset)

    # return test loss and test accuracy
    return loss, acc