import torch.nn as nn
import torch.nn.functional as F
import torch

class CNN(nn.Module):
    def __init__(self, train_shape):
        super(CNN, self).__init__()
        # Define the architecture
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
        self.pool = nn.MaxPool1d(kernel_size=2, stride=2, padding=0)
        self.fc1 = nn.Linear(128 * (train_shape // 8), 256)  # Adjust based on output of the last conv layer
        self.fc2 = nn.Linear(256, 1)  # Binary classification
        self.train_shape = train_shape

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 128 * (self.train_shape // 8))  # Flatten the tensor
        x = F.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))  # Binary output
        return x

class EnhancedCNN(nn.Module):
    def __init__(self):
        super(EnhancedCNN, self).__init__()
        
        # Define the architecture
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        self.batch_norm1 = nn.BatchNorm1d(32)
        
        self.conv2 = nn.Conv1d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        self.batch_norm2 = nn.BatchNorm1d(64)
        
        self.conv3 = nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
        self.batch_norm3 = nn.BatchNorm1d(128)
        
        self.pool = nn.MaxPool1d(kernel_size=2, stride=2, padding=0)
        
        # Global Average Pooling layer
        self.global_avg_pool = nn.AdaptiveAvgPool1d(1)
        
        # Fully connected layers
        self.fc1 = nn.Linear(128, 256)
        self.fc2 = nn.Linear(256, 1)  # Binary classification
        
        self.dropout = nn.Dropout(p=0.5)  # Dropout layer with 50% dropout rate

    def forward(self, x):
        x = F.relu(self.batch_norm1(self.conv1(x)))
        x = self.pool(x)
        
        x = F.relu(self.batch_norm2(self.conv2(x)))
        x = self.pool(x)
        
        x = F.relu(self.batch_norm3(self.conv3(x)))
        x = self.pool(x)
        
        x = self.global_avg_pool(x).view(-1, 128)  # Global Average Pooling
        
        x = F.relu(self.fc1(x))
        x = self.dropout(x)  # Apply dropout
        x = torch.sigmoid(self.fc2(x))  # Binary output
        
        return x
