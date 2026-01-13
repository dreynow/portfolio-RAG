from openai import OpenAI
from scripts.database import query_knowledge_base
import os
import httpx

VLLM_BASE_URL = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
VLLM_API_KEY = os.getenv("VLLM_API_KEY", "vllm")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "Qwen/Qwen2.5-1.5B-Instruct-GGUF")
FALLBACK_MODEL_FILE = os.getenv("FALLBACK_MODEL_FILE", "qwen2.5-1.5b-instruct-q4_k_m.gguf")

# Lazy-loaded fallback model
_llama_model = None

def is_vllm_available():
    """Check if vLLM server is reachable."""
    try:
        headers = {"Authorization": f"Bearer {VLLM_API_KEY}"}
        response = httpx.get(f"{VLLM_BASE_URL}/models", headers=headers, timeout=2.0)
        return response.status_code == 200
    except:
        return False

def get_llama_model():
    """Lazy load the llama.cpp model as fallback."""
    global _llama_model
    if _llama_model is None:
        from llama_cpp import Llama
        from huggingface_hub import hf_hub_download

        print("Loading fallback llama.cpp model...")
        model_path = hf_hub_download(
            repo_id=FALLBACK_MODEL,
            filename=FALLBACK_MODEL_FILE
        )
        _llama_model = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_threads=4,
            verbose=False
        )
        print("Fallback model loaded.")
    return _llama_model

def load_prompt(file_path, context_data):
    """Loads a text file and replaces the {context} placeholder."""
    with open(file_path, "r") as f:
        template = f.read()
    return template.format(context=context_data)

def stream_with_vllm(system_message, question):
    """Stream response using vLLM."""
    client = OpenAI(base_url=VLLM_BASE_URL, api_key=VLLM_API_KEY)
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

def stream_with_llama(system_message, question):
    """Stream response using local llama.cpp."""
    model = get_llama_model()
    prompt = f"<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n"

    for token in model(
        prompt,
        max_tokens=1024,
        temperature=0.1,
        stream=True,
        stop=["<|im_end|>"]
    ):
        text = token["choices"][0]["text"]
        if text:
            yield text

def stream_portfolio_assistant(question):
    """Stream response, falling back to llama.cpp if vLLM unavailable."""
    results = query_knowledge_base(question, n_results=5)
    context_text = "\n\n".join(results['documents'][0])

    prompt_path = os.path.join("prompts", "system_prompt.txt")
    system_message = load_prompt(prompt_path, context_text)

    if is_vllm_available():
        yield from stream_with_vllm(system_message, question)
    else:
        yield from stream_with_llama(system_message, question)

def ask_portfolio_assistant(question):
    """Non-streaming version."""
    return "".join(stream_portfolio_assistant(question))

if __name__ == "__main__":
    query = input("Ask about Dare: ")
    print("\n", ask_portfolio_assistant(query))
