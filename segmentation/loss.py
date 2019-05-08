import torch
import numpy as np
from torch.autograd import Variable
from torch.autograd.function import Function

def dice(outputs, labels):
    smooth = 1e-5
    # Having a larger smooth value can be used to avoid overfitting.
    # The larger the smooth value the closer the following term is to be 1.
    # smooth = 1

    outputs, labels = outputs.float(), labels.float()
    intersect = torch.dot(outputs, labels)
    union = torch.add(torch.sum(outputs), torch.sum(labels))
    dice = 1 - (2 * intersect + smooth) / (union + smooth)
    return dice

