import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchsummary import summary

class MobileNetV1(nn.Module):
    def __init__(self, ch_in, n_classes):
        super(MobileNetV1, self).__init__()

        def conv_bn(inp, oup, stride):
            return nn.Sequential(
                nn.Conv2d(inp, oup, 3, stride, 1, bias=False),
                nn.BatchNorm2d(oup),
                nn.ReLU(inplace=True)
                )

        def conv_dw(inp, oup, stride):
            return nn.Sequential(
                # dw
                nn.Conv2d(inp, inp, 3, stride, 1, groups=inp, bias=False),
                nn.BatchNorm2d(inp),
                nn.ReLU(inplace=True),

                # pw
                nn.Conv2d(inp, oup, 1, 1, 0, bias=False),
                nn.BatchNorm2d(oup),
                nn.ReLU(inplace=True),
                )

        self.model = nn.Sequential(
            conv_bn(ch_in, 32, 2),      # Output 16*16, RF:3
            conv_dw(32, 64, 1),         # Output 16*16, RF:7
            conv_dw(64, 128, 2),        # Output 16*16, RF:11
            conv_dw(128, 128, 1),       # Output 16*16, RF:15
            conv_dw(128, 128, 2),       # Output 8*8, RF:19
            conv_dw(128, 128, 1),       # Output 8*8, RF:27
            conv_dw(128, 128, 2),       # Output 4*4, RF:31
            conv_dw(128, 128, 1),       # Output 4*4, RF:47
            conv_dw(128, 128, 1),       # Output 4*4, RF:63
            conv_dw(128, 128, 1),       # Output 4*4, RF:79
            conv_dw(128, 128, 1),       # Output 4*4, RF:95
            nn.AdaptiveAvgPool2d(1)
        )
        self.fc = nn.Linear(128*1, n_classes)

    def forward(self, x):
        x = self.model(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x
    

if __name__ == "__main__":
    model = MobileNetV1(ch_in=3, n_classes=10)
    print(summary(model, input_size=(3, 32, 32)))