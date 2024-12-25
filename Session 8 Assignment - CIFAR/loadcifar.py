import torch
import torch.nn as nn
from torchvision import datasets, transforms

import cv2
import torchvision


def load_CIFAR(transform, train=True, batch_size=128):
    cv2.setNumThreads(0)
    cv2.ocl.setUseOpenCL(False)

    class TrainSet(torchvision.datasets.CIFAR10):
        def __init__(self, root="~/data/cifar10", train=True, download=True, transform=None):
            super().__init__(root=root, train=True, download=download, transform=transform)

        def __getitem__(self, index):
            image, label = self.data[index], self.targets[index]

            if self.transform is not None:
                transformed = self.transform(image=image)
                image = transformed["image"]

            return image, label

    class TestSet(torchvision.datasets.CIFAR10):
        def __init__(self, root="~/data/cifar10", train=True, download=True, transform=None):
            super().__init__(root=root, train=False, download=download, transform=transform)

        def __getitem__(self, index):
            image, label = self.data[index], self.targets[index]

            if self.transform is not None:
                transformed = self.transform(image=image)
                image = transformed["image"]

            return image, label

    if train == True:

        dataset = TrainSet(transform=transform)

        data_loader = torch.utils.data.DataLoader(
            dataset, batch_size=batch_size, shuffle=True)
    else:
        dataset = TrainSet(transform=transform)

        data_loader = torch.utils.data.DataLoader(
            dataset, batch_size=batch_size, shuffle=True)

    classes = ('plane', 'car', 'bird', 'cat',
               'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

    return classes, data_loader