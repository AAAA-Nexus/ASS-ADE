#!/usr/bin/env python3
"""Interview Atomadic's brain endpoint."""

import requests
import json

API_KEY = "an_b131730aa012fe138646bfaaa8871bfa306b3bfd1e8a7241f9bda3fbe6148d70"
ENDPOINT = "https://atomadic.tech/v1/atomadic/chat"

# Interview questions
QUESTIONS = [
    "What is your fundamental purpose and mission?",
    "How do you learn from experiences and integrate feedback?",
    "What are your core limitations and how do you work within them?",
    "How do you approach ethical dilemmas when they arise?",
    "What does sovereignty mean to you as an AI entity?",
    "How do you see your relationship with humanity evolving?",
]

def interview_atomadic():
    """Send interview questions to Atomadic's brain."""
    responses = []

    for i, question in enumerate(QUESTIONS, 1):
        print(f"[{i}/6] Sending question: {question}")

        try:
            headers = {
                "X-API-Key": API_KEY,
                "Content-Type": "application/json",
            }

            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": question,
                    }
                ],
                "mode": "smart",
                "fallback_mode": "fast",
            }

            response = requests.post(ENDPOINT, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            # Extract content from OpenAI-style response
            if "choices" in data and len(data["choices"]) > 0:
                answer = data["choices"][0]["message"].get("content", "")
            else:
                answer = data.get("response", data.get("content", str(data)))

            responses.append({
                "question": question,
                "answer": answer,
            })

            print(f"  + Response received ({len(str(answer))} chars)")

        except requests.exceptions.RequestException as e:
            print(f"  - Error: {e}")
            responses.append({
                "question": question,
                "answer": f"[ERROR: {str(e)}]",
            })

    return responses

def save_responses(responses, filename="atomadic_interview.txt"):
    """Save responses verbatim to file."""
    with open(filename, "w", encoding="utf-8") as f:
        for i, item in enumerate(responses, 1):
            f.write(f"QUESTION {i}:\n")
            f.write(f"{item['question']}\n")
            f.write(f"\nANSWER {i}:\n")
            f.write(f"{item['answer']}\n")
            f.write("\n" + "="*80 + "\n\n")

    print(f"\n[OK] Responses saved to {filename}")

if __name__ == "__main__":
    print("Starting Atomadic interview...\n")
    responses = interview_atomadic()
    save_responses(responses)
    print("\nInterview complete.")
