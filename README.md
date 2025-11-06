
![LaMoppe](/assets/LaMoppe.png)
# LaMoppe - Prompt safety extension

## What is LaMoppe
LaMoppe is a Firefox extension that analyzes prompts sent remotely to external companies to prevent confidential information leaks. It runs with a locally-hosted finetuned 8B Llama 3.1 model agent and incorporates a Chroma vector database for a training feedback loop based on user feedback.

## Next Steps
Short-term, the goal is to allow company-specific information to be stored in the database to enable RAG (Retrieval-Augmented Generation) operations with the agent and more precise prompt analysis. Making the analysis model smaller is also critical for the viability of the project, we aim to minimize the locally hosted model through QLoRA finetuning.
![DemoLocal](/assets/lamoppedemo.png)

![schema](/assets/schema.png)