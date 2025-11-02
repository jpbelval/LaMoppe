from llama_cpp import Llama
import yaml
from dotenv import load_dotenv
from transformers import AutoModel, AutoTokenizer

class LocalInferenceClient:
    def __init__(self, model_path, default_max_tokens=256):
        self.llm = Llama(model_path=model_path)
        self.default_max_tokens = default_max_tokens

    def generate(self, prompt, **kwargs):
        # If prompt is a ChatMessage object, extract text
        with open("./system_prompt.yaml", 'r') as stream:
            system_prompt = yaml.safe_load(stream)
        prompt = system_prompt["system_prompt"] + "/n user" + prompt

        # Handle max_tokens safely
        max_tokens = kwargs.get("max_new_tokens", self.default_max_tokens)
        try:
            max_tokens = int(max_tokens)
        except (TypeError, ValueError):
            raise ValueError(f"max_new_tokens must be an integer, got {type(max_tokens)}")

        temperature = kwargs.get("temperature", 0.7)
        top_p = kwargs.get("top_p", 1.0)
        stop_sequences = kwargs.get("stop_sequences", None)

        output = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stop=stop_sequences
        )
        print(output)
        return output
    
if __name__ == "__main__":
    load_dotenv()
    model = AutoModel.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
    model.save_pretrained("./hf_model")
    tokenizer.save_pretrained("./hf_model")
