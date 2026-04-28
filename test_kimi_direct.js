// Quick test of Kimi K2.5 direct call
import { unstable_dev } from "wrangler";

const worker = await unstable_dev("scripts/cognition_worker.js", {
  config: "scripts/wrangler.cognition.toml",
  local: true,
  ip: "127.0.0.1",
});

try {
  const res = await worker.fetch("http://127.0.0.1:8787/v1/atomadic/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": "test-key"
    },
    body: JSON.stringify({
      messages: [{ role: "user", content: "Who are you?" }],
      mode: "smart"
    })
  });

  const data = await res.json();
  console.log("Status:", res.status);
  console.log("Response:", JSON.stringify(data, null, 2));
  console.log("Content:", data.choices?.[0]?.message?.content);
} catch (err) {
  console.error("Test error:", err);
} finally {
  await worker.stop();
}
