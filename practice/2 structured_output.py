from client import client, MODEL
from pydantic import BaseModel
import json

class TriageResult(BaseModel):
    failure_type: str
    root_cause: str
    confidence: float
    fix_suggestion: str

response = client.messages.create(
    model=MODEL,
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": """Analyze this CI failure: ImportError: No module named 'requests'

Reply with ONLY a JSON object, no other text:
{
    "failure_type": "...",
    "root_cause": "...",
    "confidence": 0.0,
    "fix_suggestion": "..."
}"""
    }]
)

raw = next(block.text for block in response.content if hasattr(block, "text"))
result = TriageResult.model_validate_json(raw)

print(f"Failure type: {result.failure_type}")
print(f"Root cause: {result.root_cause}")
print(f"Confidence: {result.confidence}")
print(f"Fix suggestion: {result.fix_suggestion}")