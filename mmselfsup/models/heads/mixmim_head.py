# Copyright (c) OpenMMLab. All rights reserved.
import torch
from mmengine.model import BaseModule

from mmselfsup.registry import MODELS
from .mae_head import MAEPretrainHead
import timm.optim.optim_factory as optim_factory

@MODELS.register_module()
class MixMIMPretrainHead(MAEPretrainHead):

    def __init__(self,
                 loss: dict,
                 norm_pix: bool = False,
                 patch_size: int = 16) -> None:
        super().__init__(loss=loss, norm_pix=norm_pix, patch_size=patch_size)

    def forward(self, x_rec: torch.Tensor, target: torch.Tensor,
                mask: torch.Tensor) -> torch.Tensor:
        """Forward function of MixMIM head.

        Args:
            pred (torch.Tensor): The reconstructed image.
            target (torch.Tensor): The target image.
            mask (torch.Tensor): The mask of the target image.

        Returns:
            torch.Tensor: The reconstruction loss.
        """
        target = self.construct_target(target)

        B, L, C = x_rec.shape

        # unmix tokens
        x1_rec = x_rec[:B//2]
        x2_rec = x_rec[B//2:]

        unmix_x_rec = x1_rec * mask + x2_rec.flip(0) * (1 - mask)
        loss_rec = (unmix_x_rec - target) ** 2
        loss_rec = loss_rec.mean()

        return loss_rec