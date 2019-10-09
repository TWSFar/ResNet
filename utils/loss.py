import torch
import torch.nn as nn


class SegmentationLosses(object):
    def __init__(self, weight=None, reduction='mean', batch_average=True, ignore_index=255, cuda=False):
        self.ignore_index = ignore_index
        self.weight = weight
        self.reduction = reduction
        self.batch_average = batch_average
        self.cuda = cuda
        
    
    def build_loss(self, mode='ce'):
        if mode == 'ce':
            return self.CrossEntropyLoss
        elif mode == 'focal':
            return self.FocalLoss
        else:
            raise NotImplementedError
        
    def CrossEntropyLoss(self, logit, target):
        # n, c, h, w = logit.size()
        criterion = nn.CrossEntropyLoss(weight=self.weight, ignore_index=self.ignore_index,
                                        reduction=self.reduction)
        if self.cuda:
            criterion = criterion.cuda()
        loss = criterion(logit, target.long())
        n = 1
        if self.batch_average:
            loss /= n
        return loss
    
    def FocalLoss(self, logit, target, gamma=2, alpha=0.5):
        # n, c, h, w = logit.size()
        criterion = nn.CrossEntropyLoss(weight=self.weight, ignore_index=self.ignore_index,
                                        reduction=self.reduction)
        if self.cuda:
            criterion = criterion.cuda()
        logpt = -criterion(logit, target.long())
        pt = torch.exp(logpt)
        if alpha is not None:
            logpt *= alpha
        loss = -((1 - pt) ** gamma) * logpt
        n = 1
        if self.batch_average:
            loss /= n
        return loss

        
if __name__ == "__main__":
    loss = SegmentationLosses()
    # a = torch.randn(1, 4, 7, 7)
    # b = torch.randn(1, 7, 7)

    a = torch.tensor([[0.0, 1]])
    b = torch.tensor([1])
    print(loss.CrossEntropyLoss(a, b).item())
    print(loss.FocalLoss(a, b, gamma=0, alpha=None).item())
    print(loss.FocalLoss(a, b, gamma=2, alpha=0.5).item())
