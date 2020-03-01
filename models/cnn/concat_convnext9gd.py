"""
@author : Hyunwoong
@when : 8/25/2019
@homepage : https://github.com/gusdnd852
"""

import torch
from torch import nn


class Conv1D(nn.Module):

    def __init__(self, _in, _out, kernel_size, group):
        super(Conv1D, self).__init__()
        self.conv = nn.Conv1d(_in, _out, kernel_size=kernel_size, padding=kernel_size // 2, groups=group)
        self.batch_norm = nn.BatchNorm1d(_out)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv(x)
        x = self.batch_norm(x)
        x = self.relu(x)
        return x


class Model(nn.Module):

    def __init__(self):
        super(Model, self).__init__()

        self.conv1 = Conv1D(4, 32, 3, 2)
        self.conv2 = Conv1D(32, 64, 3, 2)
        self.pool1 = nn.MaxPool1d(kernel_size=2, stride=2)

        self.conv3 = Conv1D(96, 128, 3, 4)
        self.conv4 = Conv1D(128, 256, 3, 4)
        self.pool2 = nn.MaxPool1d(kernel_size=2, stride=2)

        self.conv5 = Conv1D(384, 512, 3, 8)
        self.conv6 = Conv1D(512, 1024, 3, 8)
        self.pool3 = nn.MaxPool1d(kernel_size=2, stride=2)

        self.conv7 = Conv1D(1536, 1536, 3, 16)
        self.conv8 = Conv1D(1536, 1536, 3, 16)
        self.pool4 = nn.MaxPool1d(kernel_size=2, stride=2)

        self.output_layer = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(6144, 1),
            nn.Sigmoid())

    def forward(self, x):
        b, c, l = x.shape
        x = self.conv1(x)
        _x = self.conv2(x)
        x = torch.cat([x, _x], dim=1)
        x = self.pool1(x)

        x = self.conv3(x)
        _x = self.conv4(x)
        x = torch.cat([x, _x], dim=1)
        x = self.pool2(x)

        x = self.conv5(x)
        _x = self.conv6(x)
        x = torch.cat([x, _x], dim=1)
        x = self.pool3(x)

        x = self.conv7(x)
        _x = self.conv8(x)
        x = torch.cat([x, _x], dim=1)
        x = self.pool4(x)

        x = x.view(b, -1)
        x = self.output_layer(x)
        return x