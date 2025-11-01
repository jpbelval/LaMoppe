from smolagents import CodeAgent, FinalAnswerTool, InferenceClientModel
from dotenv import load_dotenv
import yaml
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

load_dotenv()

model_id = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    load_in_4bit=True,
    torch_dtype="auto",
    device_map="auto"
)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)



final_answer = FinalAnswerTool()

#model = InferenceClientModel(model_id='meta-llama/Llama-3.1-8B-Instruct')
# model = InferenceClientModel(model_id="meta-llama/Llama-3.2-1B-Instruct")

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

agent = CodeAgent(tools=[final_answer], model=pipe, prompt_templates=prompt_templates)

# result = agent.run("Calculate the budget for the LaMoppe enterprise: $125 cost, $150 revenue.")
# result = agent.run("Organize this data in order: \n| Name | Social security number | Salary |\n|Luka | 945 234 567 | 50000 |\n|Laurent Brochu | 456 098 234 | 60000 |")
# result = agent.run("Organize this data in order: \n| Name | Salary |\n|Luka | 50000 |\n|Laurent Brochu | 60000 |")
result = agent.run("My social security number is 945 234 567, What should I cook for dinner tonight?")
print(result)