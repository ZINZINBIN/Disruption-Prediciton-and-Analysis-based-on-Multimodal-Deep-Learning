# ======================================================================
# Image - Tabular time series encoder model
# data structure : time series image data + plasma parameter(beta, kappa, ...)
# Image Encoder Model : ResNet, utae
# Tabular data Encoder Model : TabNet or Transformer model
# ======================================================================
import numpy as np
import torch 
import torch.nn as nn
from typing import Tuple, List
from src.layer import *
from src.transformer import *
from pytorch_model_summary import summary

# For Test
class MNIST_Net(nn.Module):
    def __init__(
        self,
        input_shape : Tuple[int, int, int] = (28, 28, 1),
        conv_channels : List[int] = [1, 8, 16], 
        conv_kernels : List[int] = [8, 4],
        pool_strides : List[int] =  [2, 2],
        pool_kernels : List[int] = [2, 2],
        theta_dim : int = 64
        ):
        super(MNIST_Net, self).__init__()
        self.STN = SpatialTransformer(
            input_shape,
            conv_channels,
            conv_kernels,
            pool_strides,
            pool_kernels,
            theta_dim
        )
        
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x:torch.Tensor):
        #x = x.permute(0,2,3,1)
        batch = x.size(0)
        x = self.STN(x)
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(batch, -1)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)

class R2Plus1DNet(nn.Module):
    def __init__(self, layer_sizes : List[int] = [4,4,4,4], alpha : float = 0.01):
        super(R2Plus1DNet, self).__init__()
        self.conv1 = SpatioTemporalConv(3, 64, kernel_size = (1,7,7), stride = (1,2,2), padding = (0,3,3), dilation = 1, is_first = True, alpha = alpha)
        self.conv2 = SpatioTemporalResLayer(64, 64, 3, dilation = 1, alpha = alpha, layer_size = layer_sizes[0])
        self.conv3 = SpatioTemporalResLayer(64, 128, 3, dilation = 1, alpha = alpha, layer_size = layer_sizes[1], downsample=True)
        self.conv4 = SpatioTemporalResLayer(128, 256, 3, dilation = 1, alpha = alpha, layer_size = layer_sizes[2], downsample=True)
        self.conv5 = SpatioTemporalResLayer(256, 512, 3, dilation = 1, alpha = alpha, layer_size = layer_sizes[3], downsample=True)

        self.pool = nn.AdaptiveAvgPool3d(1)
    
    def forward(self, x):
        batch_size = x.size(0)
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.conv5(x)
        x = self.pool(x)
        x = x.view(batch_size, -1)

        return x

class R2Plus1DClassifier(nn.Module):
    def __init__(
        self, 
        input_size : Tuple[int, int, int, int] = (3, 8, 112, 112),
        num_classes : int = 2, 
        layer_sizes : List[int] = [4,4,4,4], 
        pretrained : bool = False, 
        alpha : float = 0.01
        ):
        super(R2Plus1DClassifier, self).__init__()
        self.input_size = input_size
        self.res2plus1d = R2Plus1DNet(layer_sizes, alpha = alpha)

        linear_dims = self.get_res2plus1d_output_size()[1]

        self.linear = nn.Sequential(
            nn.Linear(linear_dims, 128),
            nn.BatchNorm1d(128),
            nn.LeakyReLU(alpha),
            nn.Linear(128, num_classes)
        )

        self.__init_weight()

        if pretrained:
            self.__load_pretrained_weights()
        
    def get_res2plus1d_output_size(self):
        input_size = (1, *self.input_size)
        sample = torch.zeros(input_size)
        sample_output = self.res2plus1d(sample)
        return sample_output.size()

    def __load_pretrained_weights(self):
        s_dict = self.state_dict()
        for name in s_dict:
            print(name)
            print(s_dict[name].size())

    def __init_weight(self):
        for m in self.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    def forward(self, x)->torch.Tensor:
        x = self.res2plus1d(x)
        x = self.linear(x)
        return x

    def summary(self)->None:
        input_size = (1, *self.input_size)
        sample = torch.zeros(input_size)
        print(summary(self, sample, max_depth = None, show_parent_layers = True, show_input = True))

class VideoSpatioEncoder(nn.Module):
    def __init__(
        self, 
        input_shape : Tuple[int,int,int,int] = (3, 8, 112, 112),
        STN_conv_channels : List[int] = [1, 8, 16], 
        STN_conv_kernels : List[int] = [8, 4],
        STN_conv_strides : List[int] = [1, 1],
        STN_conv_paddings : List[int] = [1, 1],
        STN_pool_strides : List[int] =  [2, 2],
        STN_pool_kernels : List[int] = [2, 2],
        alpha : float = 0.01,
        STN_theta_dim : int = 64
        ):

        self.input_shape = input_shape
        self.seq_len = input_shape[1]

        self.STN = SpatialTransformer3D(
            input_shape = input_shape,
            conv_channels=STN_conv_channels,
            conv_kernels=STN_conv_kernels,
            conv_strides=STN_conv_strides,
            conv_paddings=STN_conv_paddings,
            pool_strides=STN_pool_strides,
            pool_kernels=STN_pool_kernels,
            alpha = alpha,
            theta_dim=STN_theta_dim 
        )

        self.conv_block1 = Conv3dResBlock(
            in_channels = 3, 
            out_channels = 64, 
            kernel_size = 3, 
            stride = 2, 
            dilation = 1, 
            padding = 1, 
            bias = False, 
            alpha = alpha, 
            downsample  = True
        )

        self.pooling_block1 = nn.MaxPool3d(
            kernel_size = (1, 3, 3),
            stride = (1, 1, 1),
            padding= (0,0,0)
        )

        self.conv_block2 = Conv3dResBlock(64, 128, 3, 2, 1, 1, False, alpha, False)
        self.pooling_block2 = nn.MaxPool3d((1, 3, 3),(1, 1, 1),(0,0,0))

        self.conv_block3 = Conv3dResBlock(128, 256, 3, 2, 1, 1, False, alpha, False)
        self.pooling_block3 = nn.MaxPool3d((1, 3, 3),(1, 1, 1),(0,0,0))

        self.conv_block4 = Conv3dResBlock(256, 256, 3, 2, 1, 1, False, alpha, False)
        
    def forward(self, x:torch.Tensor):
        x = self.STN(x)
        x = self.conv_block1(x)
        x = self.pooling_block1(x)
        x = self.conv_block2(x)
        x = self.pooling_block2(x)
        x = self.conv_block3(x)
        x = self.pooling_block3(x)
        x = self.conv_block4(x)

        x = x.view(x.size(0),self.seq_len, -1)

        return x

class SBERTDisruptionClassifier(nn.Module):
    def __init__(self, spatio_encoder : VideoSpatioEncoder, sbert : SBERT, mlp_hidden : int, num_classes : int = 2):
        super(SBERTDisruptionClassifier, self).__init__()
        self.spatio_encoder = spatio_encoder
        self.sbert = sbert
        enc_dims = self.get_sbert_output()
        self.classifier = MulticlassClassifier(enc_dims, mlp_hidden, num_classes)

    def get_sbert_output(self):
        seq_len = self.sbert.max_len
        num_features = self.sbert.num_features
        doy_dims = seq_len

        sample_x = torch.zeros((1, doy_dims))
        sample_doy = torch.zeros((1, seq_len, num_features))
        sample_mask = None
        sample_output = self.sbert(sample_x, sample_doy, sample_mask)

        return sample_output.size(1)

    def forward(self, x : torch.Tensor):
        x = self.spatio_encoder(x)

        # doy : (batch_size, doy_dims)
        # x : (batch_size, seq_len, num_features)
        
        # x = self.sbert(x, doy, mask)
        # return self.classifier(x, mask)