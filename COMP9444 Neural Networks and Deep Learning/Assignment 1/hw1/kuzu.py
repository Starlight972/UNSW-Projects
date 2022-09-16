"""
   kuzu.py
   COMP9444, CSE, UNSW
"""

from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F

class NetLin(nn.Module):
    # linear function followed by softmax
    def __init__(self):
        super(NetLin, self).__init__()
        # INSERT CODE HERE
        self.linear = nn.Linear(784, 10)
        self.softmax = nn.LogSoftmax()

    def forward(self, x):
        x = x.view(x.shape[0], -1)
        x = self.linear(x)
        x = self.softmax(x)
        return x

class NetFull(nn.Module):
    # two fully connected tanh layers followed by log softmax
    def __init__(self):
        super(NetFull, self).__init__()
        self.hidden = nn.Linear(784, 64)
        self.output = nn.Linear(64, 10)
        self.softmax = nn.LogSoftmax()

    def forward(self, x):
        x = x.view(x.shape[0], -1)
        x = F.tanh(self.hidden(x))
        x = self.output(x)
        x = self.softmax(x)
        return x

class NetConv(nn.Module):
    # two convolutional layers and one fully connected layer,
    # all using relu, followed by softmax
    def __init__(self):
        super(NetConv, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 80, 5)
        self.linear = nn.Linear(1280, 64)
        self.output = nn.Linear(64, 10)
        self.softmax = nn.LogSoftmax()

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(x.shape[0], -1)
        x = F.tanh(self.linear(x))
        x = self.output(x)
        x = self.softmax(x)
        return x

'''
if __name__ == '__main__':
    net = NetConv()
    print('#Parameters number:', sum(param.numel() for param in net.parameters()))
'''