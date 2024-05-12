import torch.nn as nn
import torch

"""
    @class (2+1)D CNN used in detecting the presence of actions
        @param in_channels: The number of input channels to the model
        @param intermediate: The number of intermediate channels (i.e size of the input to the second block of the model)
        @param out_channels: The number of the output channels of the model
        @param kernel_size: Array containing the respective dimensions of the kernels
        @param strides: Array containing the respective convolutional stride values
"""
def count_parameters(model):
    all_params = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return all_params, trainable

class TwoPlusOneD_CNN(nn.Module):
    def __init__(self, in_channels, intermediate, out_channels, kernel_size, strides):
        super(TwoPlusOneD_CNN, self).__init__()
        self.conv_block = nn.Sequential(
            nn.Conv3d(in_channels, intermediate, kernel_size = (1, kernel_size[1], kernel_size[2]), stride = (1, strides[1], strides[2]), bias = True, padding = 'valid'),
            nn.BatchNorm3d(intermediate),
            nn.ReLU(),
            nn.Conv3d(intermediate, out_channels, kernel_size = (kernel_size[0], 1, 1), stride = (strides[0], 1, 1), bias = True, padding = 'valid')
        )
        
        
    def forward(self, x):
        return self.conv_block(x)
    
class FullyConnectedNet(nn.Module):
    def __init__(self, input_size, size_1, size_2, size_3, n_classes):
        super(FullyConnectedNet, self).__init__()
        self.fcn = nn.Sequential(
            nn.Linear(input_size, size_1),
            nn.LeakyReLU(),
            nn.BatchNorm1d(size_1),
            nn.Dropout(0.1),
            nn.Linear(size_1, n_classes),
        )
        
    def forward(self, x):
        return self.fcn(x)

class SSBDModel1(nn.Module):
    def __init__(self, in_channels, intermediate, 
                 out_channels, kernel_size, strides, pooling_size, 
                 pooling_strides, size_1, size_2, size_3):
        super(SSBDModel1, self).__init__()
        
        self.net = nn.Sequential(
            TwoPlusOneD_CNN(in_channels, intermediate,  
                            out_channels, kernel_size, strides),
            nn.MaxPool3d(kernel_size = pooling_size, stride = pooling_strides),
            nn.Flatten(),
            nn.Dropout(0.4),
            FullyConnectedNet(311296, size_1, size_2, size_3, 1)
        )

    def forward(self, x):
            return self.net(x)