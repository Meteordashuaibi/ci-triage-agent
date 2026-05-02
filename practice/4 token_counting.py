from client import client, MODEL

response = client.messages.create(
    model=MODEL,
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": '"What is 2+2?"'
    }]
)
print(f"Total: {response.usage.input_tokens + response.usage.output_tokens}")