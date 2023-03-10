import torch
from typing import Tuple, List, Optional

from seq_graph_retro.utils.parse import ReactionInfo
from seq_graph_retro.data import BaseDataset, EvalDataset

class SingleEditSharedDataset(BaseDataset):

    def collater(self, attributes: List[Tuple[torch.tensor]]) -> Tuple[torch.Tensor]:
        assert isinstance(attributes, list)
        assert len(attributes) == 1
        attributes = attributes[0]
        prod_inputs, edit_labels, frag_inputs, lg_labels, lengths, bg_inputs = attributes
        return prod_inputs, bg_inputs, frag_inputs, edit_labels, lg_labels, lengths

class SharedEvalDataset(EvalDataset):

    def collater(self, attributes: List[ReactionInfo]) -> Tuple[str, List[str], List[str], Optional[List[int]]]:
        info_batch, label_batch = list(zip(*attributes))
        prod_smi = [info.rxn_smi.split(">>")[-1] for info in info_batch]
        core_edits = [set(info.core_edits) for info in info_batch]
        if self.use_rxn_class:
            rxn_classes = [info.rxn_class for info in info_batch]
            return prod_smi, core_edits, label_batch, rxn_classes
        else:
            return prod_smi, core_edits, label_batch, None
