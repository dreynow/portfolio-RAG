from openai import OpenAI
from scripts.database import query_knowledge_base
import os

VLLM_BASE_URL = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
client = OpenAI(base_url=VLLM_BASE_URL, api_key="vllm")

def load_prompt(file_path, context_data):
    """Loads a text file and replaces the {context} placeholder."""
    with open(file_path, "r") as f:
        template = f.read()
    return template.format(context=context_data)

def ask_portfolio_assistant(question):
    # 1. Get data from ChromaDB
    results = query_knowledge_base(question, n_results=5)
    context_text = "\n\n".join(results['documents'][0])

    # 2. Load the external prompt and inject context
    prompt_path = os.path.join("prompts", "system_prompt.txt")
    system_message = load_prompt(prompt_path, context_text)

    # 3. Send to vLLM
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content


def stream_portfolio_assistant(question):
    results = query_knowledge_base(question, n_results=5)
    context_text = "\n\n".join(results['documents'][0])

    prompt_path = os.path.join("prompts", "system_prompt.txt")
    system_message = load_prompt(prompt_path, context_text)

    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ],
        temperature=0.1,
        stream=True 
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


if __name__ == "__main__":
    query = input("Ask about Dare: ")
    print("\n", ask_portfolio_assistant(query))