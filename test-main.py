from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="" 
)

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[{"role": "user", "content": "You are my portfolio assistant. Who am I?"}]
)

print(response.choices[0].message.content)