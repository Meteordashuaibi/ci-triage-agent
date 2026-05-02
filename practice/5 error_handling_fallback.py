from client import client
print(client)
try:
    response = client.messages.create(
        model="fake-model-xyz",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": "What is 2+2?"
        }]
    )
except Exception as e:
    print(f"API failed: {e}")
    response = "fallback default result"

print(response)