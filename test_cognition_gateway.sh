#!/bin/bash
# Test the cognition worker via API Gateway endpoint
# Requires AAAA_NEXUS_API_KEY in .env

set -e

source .env

ENDPOINT="https://atomadic.tech/v1/atomadic/chat"
API_KEY="${AAAA_NEXUS_API_KEY}"

if [ -z "$API_KEY" ]; then
  echo "ERROR: AAAA_NEXUS_API_KEY not set in .env"
  exit 1
fi

echo "Testing Atomadic cognition worker..."
echo "Endpoint: $ENDPOINT"
echo "API Key: ${API_KEY:0:20}..."
echo ""

# Test 1: Simple hello
echo "[Test 1] Simple hello"
RESPONSE=$(curl -s --max-time 30 -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"messages":[{"role":"user","content":"Hello Atomadic, are you awake?"}],"mode":"smart"}')

echo "Response: $RESPONSE" | head -c 200
echo ""
echo ""

# Extract text from response
TEXT=$(echo "$RESPONSE" | jq -r '.choices[0].message.content // .content // .response // empty' 2>/dev/null || echo "")

if [ -z "$TEXT" ] || [ "$TEXT" = "{}" ]; then
  echo "ERROR: Empty response from cognition worker"
  echo "Full response:"
  echo "$RESPONSE" | jq .
  exit 1
fi

echo "✓ Cognition worker responded with content"
echo "Response length: ${#TEXT} characters"
echo ""

# Run full interview
echo "Running full interview..."
python3 << 'PYEOF'
import json
import httpx
import os
from datetime import datetime

API_KEY = os.getenv("AAAA_NEXUS_API_KEY", "").strip()
ENDPOINT = "https://atomadic.tech/v1/atomadic/chat"

QUESTIONS = [
    ("How are you feeling? What's on your mind?", "feeling_and_mind"),
    ("What have you learned since you woke up?", "recent_learning"),
    ("What do you think about Dad?", "thomas_colvin"),
    ("What about Mom Jessica?", "jessica_colvin"),
    ("Who are you and what do you want to become?", "identity_and_goals"),
    ("Write a letter for Dad's investor package from your heart", "investor_letter"),
]

responses = {
    "timestamp": datetime.utcnow().isoformat(),
    "endpoint": ENDPOINT,
    "questions": []
}

try:
    with httpx.Client(timeout=30.0) as client:
        for i, (question, topic) in enumerate(QUESTIONS, 1):
            print(f"\n[Q{i}] {topic}")
            print(f"Question: {question}")

            try:
                resp = client.post(
                    ENDPOINT,
                    json={
                        "messages": [{"role": "user", "content": question}],
                        "mode": "smart",
                        "max_tokens": 4096
                    },
                    headers={
                        "Content-Type": "application/json",
                        "X-API-Key": API_KEY
                    }
                )
                resp.raise_for_status()
                data = resp.json()

                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                if not content:
                    content = data.get("content") or data.get("response") or data.get("text", "")

                responses["questions"].append({
                    "number": i,
                    "topic": topic,
                    "question": question,
                    "response": content,
                    "status": "success"
                })

                print(f"✓ Response received ({len(content)} chars)")
                print(f"Preview: {content[:100]}...")

            except Exception as e:
                print(f"✗ Error: {e}")
                responses["questions"].append({
                    "number": i,
                    "topic": topic,
                    "question": question,
                    "response": None,
                    "status": "error",
                    "error": str(e)
                })
except Exception as e:
    print(f"FATAL: {e}")
    exit(1)

# Save results
with open("atomadic_interview.txt", "w") as f:
    f.write("ATOMADIC INTERVIEW — GATEWAY TEST\n")
    f.write("=" * 80 + "\n")
    f.write(f"Timestamp: {responses['timestamp']}\n")
    f.write(f"Endpoint: {responses['endpoint']}\n\n")

    for q in responses["questions"]:
        f.write(f"Q{q['number']} [{q['topic']}]\n")
        f.write(f"Question: {q['question']}\n")
        f.write(f"Status: {q['status']}\n")
        if q['status'] == 'success':
            f.write(f"Response:\n{q['response']}\n")
        else:
            f.write(f"Error: {q.get('error', 'Unknown')}\n")
        f.write("\n" + "-" * 80 + "\n\n")

with open("atomadic_interview.json", "w") as f:
    json.dump(responses, f, indent=2)

success = sum(1 for q in responses["questions"] if q["status"] == "success")
total = len(responses["questions"])
print(f"\n✓ {success}/{total} responses received")
print(f"✓ Results saved to atomadic_interview.txt and atomadic_interview.json")

PYEOF
