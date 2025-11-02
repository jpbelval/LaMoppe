from smolagents import TransformersModel
from transformers import StoppingCriteria, StoppingCriteriaList

class StopSequencesCriteria(StoppingCriteria):
    def __init__(self, stop_token_ids):
        self.stop_token_ids = stop_token_ids

    def __call__(self, input_ids, scores, **kwargs):
        for seq in self.stop_token_ids:
            if input_ids[0, -len(seq):].tolist() == seq:
                return True
        return False

class TransformersModelWithStopSequences(TransformersModel):
    def generate(self, prompt, **kwargs):
        stop_sequences = kwargs.pop("stop_sequences", None)

        stopping_criteria = kwargs.pop("stopping_criteria", None)

        if stop_sequences is not None:
            stop_token_ids = [
                self.tokenizer(seq, add_special_tokens=False)["input_ids"]
                for seq in stop_sequences
            ]
            stop_criteria = StopSequencesCriteria(stop_token_ids)
            if stopping_criteria is not None:
                stopping_criteria.append(stop_criteria)
            else:
                stopping_criteria = StoppingCriteriaList([stop_criteria])
            kwargs["stopping_criteria"] = stopping_criteria

        return super().generate(prompt, **kwargs)
