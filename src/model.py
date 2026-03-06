# Responsibilities:
# - Define model architecture
# - Load pretrained weights
# - Modify final layer for N species

import torchvision.models as models
import torch.nn as nn

class Model:
    def __init__(self): ...

    def build_model(self, num_classes):
        model = models.efficientnet_b0(weights='IMAGENET1K_V1')
        model.classifier[1] = nn.Linear(
            model.classifier[1].in_features,
            num_classes
        )
        return model