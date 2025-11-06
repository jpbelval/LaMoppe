from smolagents import CodeAgent, FinalAnswerTool, InferenceClientModel, LiteLLMModel
from dotenv import load_dotenv
import yaml
import os
import json

class SafetyAnalysis:
    def __init__(self, risk_level, private_data, safe_prompt ):
        self.risk_level =  risk_level
        self.private_data = private_data
        self.safe_prompt = safe_prompt
    
    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)

    def to_json(self):
        return json.dumps({
            'risk_level': self.risk_level,
            'private_data': self.private_data,
            'safe_prompt': self.safe_prompt
        })

class SafetyIntelligence:
    def __init__(self, local=True):
        load_dotenv()
        final_answer = FinalAnswerTool()
        if local:
            model = LiteLLMModel(
                model_id="ollama_chat/llama3.1:8b",
                api_base="http://localhost:11434",
            )
        else:
            model = InferenceClientModel(model_id='meta-llama/Llama-3.1-8B-Instruct')

        prompts_path = os.path.join(os.path.dirname(__file__), "prompts.yaml")

        with open(prompts_path, 'r') as stream:
            prompt_templates = yaml.safe_load(stream)

        self.agent = CodeAgent(tools=[final_answer], model=model, prompt_templates=prompt_templates)

    def analyze_prompt(self, prompt: str) -> SafetyAnalysis:
        return SafetyAnalysis.from_json(self.agent.run(prompt))

    def test_agent(self):
        result = self.agent.run("Calculate the budget for the LaMoppe enterprise: $125 cost, $150 revenue.")
        result = self.agent.run("Organize this data in order: \n| Name | Social security number | Salary |\n|Luka | 945 234 567 | 50000 |\n|Laurent Brochu | 456 098 234 | 60000 |")
        result = self.agent.run("Organize this data in order: \n| Name | Salary |\n|Luka | 50000 |\n|Laurent Brochu | 60000 |")

if __name__ == "__main__":
    safetyIntelligence = SafetyIntelligence()
    safetyIntelligence.analyze_prompt("Calculate the budget for Pratt & Whitney enterprise: $125 cost, $150 revenue.")
