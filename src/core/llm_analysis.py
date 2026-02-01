import json
from openai import OpenAI

client = OpenAI()

def analyze_clause(clause_text: str) -> dict:
    prompt = f"""
You are a legal analyst.

Analyze this clause:
{clause_text}

Return ONLY JSON:
{
  "type": "...",
  "risk": "...",
  "explanation": "...",
  "suggestion": "..."
}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    return json.loads(content)
