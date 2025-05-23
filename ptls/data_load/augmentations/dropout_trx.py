import numpy as np
from ptls.data_load.feature_dict import FeatureDict


class DropoutTrx(FeatureDict):
    """
    This class is used as 'f_augmentation' argument for
    ptls.data_load.datasets.augmentation_dataset.AugmentationDataset (AugmentationIterableDataset).
    """
    def __init__(self, trx_dropout: float):
        super().__init__()
        self.trx_dropout = trx_dropout

    def __call__(self, x: dict) -> dict:
        seq_len = FeatureDict.get_seq_len(x)

        idx = self.get_idx(seq_len)
        new_x = self.seq_indexing(x, idx)
        return new_x

    def get_idx(self, seq_len: int) -> np.ndarray:
        if self.trx_dropout > 0 and seq_len > 0:
            idx = np.random.choice(seq_len,
                                   size=int(seq_len * (1 - self.trx_dropout)+1),
                                   replace=False)
            return np.sort(idx)
        return np.arange(seq_len)
