from client import client, MODEL

tools = [
    {
        "name": "get_file_content",
        "description": "Read the content of a file given its path",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to read"}
            },
            "required": ["path"]
        }
    }
]

response = client.messages.create(
    model=MODEL,
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "Please read the file at src/main.py"}
    ]
)

print("MODEL used:", MODEL)
print("stop_reason:", response.stop_reason)
print("content:", response.content)

for block in response.content:
    if block.type == "tool_use":
        tool_name = block.name   
        tool_input = block.input 
        tool_use_id = block.id 


        fake_result = f"def main():\n    print('hello world')"


        response2 = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=tools,
            messages=[
                {"role": "user", "content": "Please read the file at src/main.py"},
                {"role": "assistant", "content": response.content},
                {"role": "user", "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_id, 
                        "content": fake_result 
                    }
                ]}
            ]
        )
        print("\n--- final answer ---")
        for b in response2.content:
            if b.type == "text":
                print(b.text)
                