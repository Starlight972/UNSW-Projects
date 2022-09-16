"""
   frac.py
   COMP9444, CSE, UNSW
"""

import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import torch.nn.functional as F


class Full2Net(torch.nn.Module):
    def __init__(self, hid):
        super(Full2Net, self).__init__()
        self.hid1_layer = nn.Linear(2, hid)
        self.hid2_layer = nn.Linear(hid, hid)
        self.output_layer = nn.Linear(hid, 1)

    def forward(self, input):
        self.hid1 = torch.tanh(self.hid1_layer(input))
        self.hid2 = torch.tanh(self.hid2_layer(self.hid1))
        return torch.sigmoid(self.output_layer(self.hid2))


class Full3Net(torch.nn.Module):
    def __init__(self, hid):
        super(Full3Net, self).__init__()
        self.hid1_layer = nn.Linear(2, hid)
        self.hid2_layer = nn.Linear(hid, hid)
        self.hid3_layer = nn.Linear(hid, hid)
        self.output_layer = nn.Linear(hid, 1)

    def forward(self, input):
        self.hid1 = torch.tanh(self.hid1_layer(input))
        self.hid2 = torch.tanh(self.hid2_layer(self.hid1))
        self.hid3 = torch.tanh(self.hid3_layer(self.hid2))
        return torch.sigmoid(self.output_layer(self.hid3))


class DenseNet(torch.nn.Module):
    def __init__(self, num_hid):
        super(DenseNet, self).__init__()
        self.w10 = nn.Parameter(torch.Tensor(num_hid, 2))
        self.b1 = nn.Parameter(torch.Tensor(num_hid))

        self.w20 = nn.Parameter(torch.Tensor(num_hid, 2))
        self.w21 = nn.Parameter(torch.Tensor(num_hid, num_hid))
        self.b2 = nn.Parameter(torch.Tensor(num_hid))

        self.w30 = nn.Parameter(torch.Tensor(1, 2))
        self.w31 = nn.Parameter(torch.Tensor(1, num_hid))
        self.w32 = nn.Parameter(torch.Tensor(1, num_hid))
        self.bout = nn.Parameter(torch.Tensor(1))

    def forward(self, input):
        self.hid1 = torch.tanh(F.linear(input, self.w10, self.b1))
        self.hid2 = torch.tanh(F.linear(self.hid1, self.w21, self.b2) + F.linear(input, self.w20))
        return torch.sigmoid(F.linear(self.hid2, self.w32, self.bout) + F.linear(self.hid1, self.w31) + F.linear(input, self.w30))


if __name__ == '__main__':
    net = DenseNet(14)
    print('#Parameters number:', sum(param.numel() for param in net.parameters()))