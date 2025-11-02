from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
import json
import numpy as np


model_name = "meta-llama/Llama-3.2-1B-Instruct"
dataset = load_dataset("json", data_files="dataset.json")

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token


quantization_config = BitsAndBytesConfig(load_in_8bit=True)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=quantization_config,
    device_map="auto",
)

model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
)
model = get_peft_model(model, lora_config)
model.gradient_checkpointing_enable()
model.config.use_cache = False

def preprocess_function(examples):
    prompts = examples["prompt"]
    outputs = examples["output"]

    texts = []
    for prompt, output in zip(prompts, outputs):
        text = prompt + "\n" + json.dumps(output)
        texts.append(text)
    tokenized = tokenizer(texts, truncation=True, padding="max_length", max_length=1024)
    tokenized["labels"] = np.where(
        np.array(tokenized["attention_mask"]) == 1,
        tokenized["input_ids"],
        -100,
    )
    return tokenized

tokenized_dataset = dataset.map(preprocess_function, batched=True)

args = TrainingArguments(
    output_dir="./output",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=1,
    optim="paged_adamw_8bit",
)

trainer = Trainer(model=model, args=args, train_dataset=tokenized_dataset["train"])
trainer.train()
model.save_pretrained("./lora-llama1b-prompt-safety")