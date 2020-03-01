"""
@author : Hyunwoong
@when : 8/25/2019
@homepage : https://github.com/gusdnd852
"""
import torch
from torch import nn


class Conv1D(nn.Module):

    def __init__(self, _in, _out, kernel_size):
        super(Conv1D, self).__init__()
        self.conv = nn.Conv1d(_in, _out, kernel_size=kernel_size, padding=kernel_size // 2, groups=1)
        self.batch_norm = nn.BatchNorm1d(_out)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv(x)
        x = self.batch_norm(x)
        return self.relu(x)


class Base(nn.Module):
    def __init__(self):
        super(Base, self).__init__()
        self.conv1 = Conv1D(2, 16, kernel_size=3)
        self.conv2 = Conv1D(16, 32, kernel_size=3)
        self.pool1 = nn.MaxPool1d(kernel_size=2, stride=2)

        self.conv3 = Conv1D(48, 96, kernel_size=3)
        self.conv4 = Conv1D(96, 128, kernel_size=3)
        self.pool2 = nn.MaxPool1d(kernel_size=2, stride=2)

        self.conv5 = Conv1D(224, 512, kernel_size=3)
        self.conv6 = Conv1D(512, 1024, kernel_size=3)
        self.pool3 = nn.MaxPool1d(kernel_size=2, stride=2)

    def forward(self, x):
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
        return x


class Model(nn.Module):

    def __init__(self):
        super().__init__()
        self.left = Base()
        self.right = Base()

        self.output_layer = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(12288, 1),
            nn.Sigmoid())

    def forward(self, x):
        b, c, l = x.shape
        left = x[:, :c // 2, :]
        left = self.left(left)

        right = x[:, c // 2:, :]
        right = self.left(right)

        x = torch.cat([left, right], dim=1)
        x = x.view(b, -1)
        x = self.output_layer(x)
        return x