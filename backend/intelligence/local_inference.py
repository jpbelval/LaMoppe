import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class LocalInferenceClient:
    def __init__(self, model, tokenizer, **generate_kwargs):
        self.model = model
        self.tokenizer = tokenizer
        
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
            self.model.config.pad_token_id = self.model.config.eos_token_id

        self.generate_kwargs = {
            "max_new_tokens": 2000,
            "pad_token_id": self.tokenizer.pad_token_id,
            **generate_kwargs
        }

    def __call__(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        

        input_length = inputs["input_ids"].shape[1]

        with torch.no_grad():
            outputs = self.model.generate(**inputs, **self.generate_kwargs)
        

        new_tokens = outputs[0][input_length:]
        
        return self.tokenizer.decode(new_tokens, skip_special_tokens=True)

    
