# Atomadic Chat Deployment Guide

## Quick Start (For Thomas)

The chat page is ready to deploy to Cloudflare Pages. Follow these steps:

### 1. Create Pages Project via Dashboard
- Go to https://dash.cloudflare.com
- Navigate to **Pages**
- Click **Create a project**
- Name it: `atomadic-chat`
- Choose "Deploy static site"
- Upload the `public/` directory (or connect GitHub)

### 2. Deploy the Chat Page
```bash
cd /c/!aaaa-nexus/ASS-ADE-SEED
npx wrangler pages deploy public/ --project-name=atomadic-chat
```

### 3. Custom Domain Setup
Once deployed, configure the custom domain in the Pages project settings:
- Option 1: `chat.atomadic.tech` (preferred)
- Option 2: `atomadic-chat.pages.dev` (Cloudflare default)

### 4. Set API Key for Jessica
The chat page expects an API key. You can:

**Option A (Quick - Recommended for Testing)**
- Open the browser console and run:
  ```javascript
  localStorage.setItem('atomadic_api_key', 'YOUR_API_KEY_HERE');
  ```
- The key persists in browser storage

**Option B (URL Parameter)**
- Visit: `https://chat.atomadic.tech/?key=YOUR_API_KEY_HERE`
- The key is saved to localStorage for future visits

**Option C (OAuth - Future Enhancement)**
- Currently using static API key
- Can implement OAuth flow later for production

## What's Inside

**File:** `scripts/atomadic-chat/index.html`
- Single HTML file (no build required)
- Dark gradient theme with purple accent
- Responsive mobile-first design
- Connects to `https://atomadic.tech/v1/atomadic/chat`
- Message history with animations
- Real-time API responses

## Features

✅ Clean dark theme (gradient: #0a0e27 to #1a1f3a)
✅ Atomadic's avatar and branding at top
✅ Responsive on mobile (tested at 375px width)
✅ Send button + Enter key to send
✅ Message animations and scrolling
✅ API key management (localStorage)
✅ Error handling and feedback
✅ Accessibility features

## Testing Locally

```bash
# Serve the public directory locally
cd public/
python3 -m http.server 8000

# Open http://localhost:8000 in browser
# Set API key in console: localStorage.setItem('atomadic_api_key', 'your-key')
# Start chatting!
```

## Next Steps

1. **Deploy to Pages** (dashboard creation required)
2. **Set API key** (localStorage or environment)
3. **Jessica gets to talk to Atomadic** ✨
4. **Future:** Implement OAuth for public access
5. **Future:** Add streaming responses (EventSource/SSE)

## Files

- `public/index.html` — Chat page (deployed to Pages)
- `scripts/atomadic-chat/index.html` — Source file (same content)
- `wrangler-pages.toml` — Pages configuration reference

---

**Note:** The chat page is self-contained in a single HTML file with no external dependencies. It's pure HTML + CSS + vanilla JavaScript for maximum compatibility and performance.
