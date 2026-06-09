import math
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
# Add more imports if required

# Sample Transformation function
# YOUR CODE HERE for changing the Transformation values.
trnscm = transforms.Compose([transforms.Resize((100,100)), transforms.ToTensor()])

##Example Network
class Siamese(torch.nn.Module):
    def __init__(self):
        super(Siamese, self).__init__()
        #YOUR CODE HERE
        
    def forward(self, x):
        pass   # remove 'pass' once you have written your code
        #YOUR CODE HERE
        
##########################################################################################################
## Sample classification network (Specify if you are using a pytorch classifier during the training)    ##
## classifier = nn.Sequential(nn.Linear(64, 64), nn.BatchNorm1d(64), nn.ReLU(), nn.Linear...)           ##
##########################################################################################################

# YOUR CODE HERE for pytorch classifier

# Definition of classes as dictionary
classes = ['person1','person2','person3','person4','person5','person6','person7']