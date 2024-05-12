import torch.nn as nn
import torch
import torchvision.models as models
import torch.nn.functional as F


"""
    @class Prefetch
        Used to classify YOLO bounding boxes as adults or children
        This model was used as a part of preprocessing.
        @component VGG-19 base CNN model
        @component Fully-connected NN
        
        @param dropout_rate: The dropout rate used by the model
            @default 0.40
        @param dim_fc_layer_1: The dimension of the first hidden layer
            @default 256
        @param dim_fc_layer_2: The dimension of the second hidden layer
            @default 64
"""
class PreFetchNet(nn.Module):
    def __init__(self, dropout_rate = 0.40, dim_fc_layer_1 = 256, dim_fc_layer_2 = 64):
        super(PreFetchNet, self).__init__()

        self.baseline = models.vgg19_bn(weights='IMAGENET1K_V1')
        
        for param in self.baseline.parameters():
            param.requires_grad = False
        for param in self.baseline.classifier.parameters():
            param.requires_grad = False
            
        self.dropout_rate = dropout_rate
        self.dim_fc_layer_1 = dim_fc_layer_1
        self.dim_fc_layer_2 = dim_fc_layer_2

        # FC Layer
        self.fc1 = nn.Linear(1000, self.dim_fc_layer_1)
        self.dropout1 = nn.Dropout(self.dropout_rate)
        self.batchnorm1 = nn.BatchNorm1d(self.dim_fc_layer_1)
        self.fc2 = nn.Linear(self.dim_fc_layer_1, self.dim_fc_layer_2)
        self.dropout2 = nn.Dropout(self.dropout_rate)
        self.batchnorm2 = nn.BatchNorm1d(self.dim_fc_layer_2)
        self.fc3 = nn.Linear(self.dim_fc_layer_2, 2)

    def forward(self, x):
        # Get the R^1000 weight vector from the base model
        x = self.baseline(x)

        # Fully-connected classifier network
        x = F.sigmoid(self.fc1(x))
        x = self.dropout1(x)
        x = self.batchnorm1(x)
        x = F.sigmoid(self.fc2(x))
        x = self.dropout2(x)
        x = self.batchnorm2(x)
        x = F.relu(self.fc3(x))
        x = torch.sigmoid(x)
        return x
    
import torchvision.transforms as transforms
from PIL import Image

image_path = '/home/pranav/Desktop/baby.png'
image = Image.open(image_path)

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize to fit VGG-19 input size
    transforms.ToTensor(),           # Convert to tensor
])

# Preprocess the image
input_tensor = preprocess(image)
# Add batch dimension
input_tensor = input_tensor.unsqueeze(0)
# Add channel dimension
input_tensor = torch.cat([input_tensor] * 3, dim=1)

# Load the model
model = PreFetchNet()

# Set the model to evaluation mode
model.eval()

# Perform inference
with torch.no_grad():
    output = model(input_tensor)

# Interpret the output
probabilities = torch.softmax(output, dim=1)
predicted_class = torch.argmax(probabilities, dim=1).item()

# Print the result
print("Predicted class:", predicted_class)
