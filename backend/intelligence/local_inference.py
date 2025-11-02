import yaml

class LocalInferenceClient:
    def __init__(self, model, tokenizer, **generate_kwargs):
        self.model = model
        self.tokenizer = tokenizer
        self.generate_kwargs = {"max_new_tokens": 256, **generate_kwargs}

    def __call__(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, **self.generate_kwargs)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    
