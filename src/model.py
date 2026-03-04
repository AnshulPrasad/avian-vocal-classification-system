# Responsibilities:
# - Define model architecture
# - Load pretrained weights
# - Modify final layer for N species

import torchvision.models as models
import torch.nn as nn

def build_model(num_classes: int):
    model = models.efficientnet_b0(weights='IMAGENET1K_V1')
    model.classifier[1] = nn.Linear(
        model.classifier[1].in_features,
        num_classes
    )
    return model