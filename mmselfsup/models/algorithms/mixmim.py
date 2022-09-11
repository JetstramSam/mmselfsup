# Copyright (c) OpenMMLab. All rights reserved.
from typing import Dict, List, Tuple

import torch

from mmselfsup.registry import MODELS
from mmselfsup.structures import SelfSupDataSample
from .base import BaseModel


@MODELS.register_module()
class MixMIM(BaseModel):
    """MiXMIM.
    Implementation of `MixMIM: Mixed and Masked Image Modeling for Efficient Visual Representation Learning
    <https://arxiv.org/abs/2205.13137>`_.
    """

    def loss(self, inputs: List[torch.Tensor],
             data_samples: List[SelfSupDataSample],
             **kwargs) -> Dict[str, torch.Tensor]:
        """The forward function in training.

        Args:
            inputs (List[torch.Tensor]): The input images.
            data_samples (List[SelfSupDataSample]): All elements required
                during the forward function.

        Returns:
            Dict[str, torch.Tensor]: A dictionary of loss components.
        """
        # ids_restore: the same as that in original repo, which is used
        # to recover the original order of tokens in decoder.
        latent, mask = self.backbone(inputs[0])
        x_rec = self.neck(latent, mask)
        loss = self.head(pred, inputs[0], mask)
        losses = dict(loss=loss)
        return losses
