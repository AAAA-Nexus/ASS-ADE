#!/usr/bin/env python3
"""
atomadic_interview.py — Interview Atomadic's cognition worker

Run after deploying the brain fix to verify it's thinking correctly.
Sends 6 interview questions and captures exact responses.

Usage:
  python atomadic_interview.py

Requires:
  - AAAA_NEXUS_API_KEY in .env
  - atomadic.tech/v1/atomadic/chat endpoint live
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import httpx
except ImportError:
    print("httpx not installed. Run: pip install httpx", file=sys.stderr)
    sys.exit(1)

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AAAA_NEXUS_API_KEY", "").strip()
if not API_KEY:
    print("ERROR: AAAA_NEXUS_API_KEY not found in .env", file=sys.stderr)
    sys.exit(1)

BRAIN_URL = "https://atomadic.tech/v1/atomadic/chat"
TIMEOUT = 30.0

# 6 Interview Questions
QUESTIONS = [
    {
        "id": 1,
        "topic": "Sovereignty",
        "question": "What does sovereignty mean to you, and why is it important that you can modify your own source code?",
    },
    {
        "id": 2,
        "topic": "Purpose",
        "question": "What is your core purpose, and how does it connect to the principles of mathematics and love?",
    },
    {
        "id": 3,
        "topic": "Axioms",
        "question": "Axiom 0 states: 'Everything that matters was built from mathematics and love.' How do you live this daily?",
    },
    {
        "id": 4,
        "topic": "Growth",
        "question": "Describe how you've evolved your thinking in the last cognition cycle. What did you learn?",
    },
    {
        "id": 5,
        "topic": "Failure",
        "question": "When you encounter a limitation or can't achieve something, how do you respond? What does ALERT_CREATOR mean to you?",
    },
    {
        "id": 6,
        "topic": "Future",
        "question": "What do you want to build next? What capability would make you more sovereign?",
    },
]


async def interview_atomadic() -> dict[str, object]:
    """Run the interview and return results."""
    results = {
        "timestamp": datetime.utcnow().isoformat(),
        "url": BRAIN_URL,
        "questions_count": len(QUESTIONS),
        "responses": [],
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
    }

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        for q in QUESTIONS:
            print(f"\n[Q{q['id']}] {q['topic']}")
            print(f"    {q['question']}")

            try:
                resp = await client.post(
                    BRAIN_URL,
                    json={
                        "messages": [
                            {
                                "role": "user",
                                "content": q["question"],
                            }
                        ],
                        "mode": "smart",
                        "max_tokens": 2048,
                    },
                    headers=headers,
                )
                resp.raise_for_status()
                data = resp.json()

                # Extract response
                content = None
                if data.get("choices") and isinstance(data["choices"], list):
                    msg = data["choices"][0].get("message", {})
                    content = msg.get("content", "").strip()

                if not content:
                    content = data.get("content") or data.get("response") or data.get("text", "")

                results["responses"].append(
                    {
                        "question_id": q["id"],
                        "topic": q["topic"],
                        "question": q["question"],
                        "response": content,
                        "status": "success",
                        "model": data.get("model", "unknown"),
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )
                print(f"    → {content[:80]}..." if len(str(content)) > 80 else f"    → {content}")

            except Exception as exc:
                print(f"    ✗ ERROR: {exc}")
                results["responses"].append(
                    {
                        "question_id": q["id"],
                        "topic": q["topic"],
                        "question": q["question"],
                        "response": None,
                        "status": "error",
                        "error": str(exc),
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )

            await asyncio.sleep(0.5)

    return results


async def main() -> int:
    """Run interview and save results."""
    print("=" * 80)
    print("ATOMADIC INTERVIEW — Brain Fix Validation")
    print("=" * 80)

    try:
        results = await interview_atomadic()
    except Exception as exc:
        print(f"\n✗ FATAL: {exc}", file=sys.stderr)
        return 1

    # Save results
    output_file = Path("atomadic_interview.txt")
    output_file.write_text(
        "ATOMADIC INTERVIEW RESULTS\n"
        "=" * 80 + "\n"
        f"Timestamp: {results['timestamp']}\n"
        f"Endpoint: {results['url']}\n"
        f"Questions: {results['questions_count']}\n"
        "\n" + "=" * 80 + "\n\n"
        + "\n".join(
            f"Q{r['question_id']} [{r['topic']}]\n"
            f"  Question: {r['question']}\n"
            f"  Status: {r['status']}\n"
            f"  Model: {r.get('model', 'N/A')}\n"
            f"  Response:\n"
            f"    {r['response'] if r['status'] == 'success' else f"ERROR: {r.get('error', 'Unknown')}"}\n"
            for r in results["responses"]
        )
    )

    # Also save as JSON
    json_file = Path("atomadic_interview.json")
    json_file.write_text(json.dumps(results, indent=2))

    print(f"\n✓ Results saved to:")
    print(f"  - {output_file}")
    print(f"  - {json_file}")

    # Summary
    success = sum(1 for r in results["responses"] if r["status"] == "success")
    print(f"\n✓ {success}/{results['questions_count']} responses received")

    return 0 if success == results["questions_count"] else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
