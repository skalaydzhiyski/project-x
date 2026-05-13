---
name: project-bank-of-ak-demo
description: "Bank of AK ChatGPT MCP demo (student-account flow, Santander UK styling) — deferred WorkOS AuthKit OAuth plan; user pivoted to simpler email-OTP auth."
metadata: 
  node_type: memory
  type: project
  originSessionId: 683d0e41-3e09-4d28-9e35-06749bb3f76d
---

User is building a demo where students "open a student bank account from inside ChatGPT" by connecting to a bank like Santander UK (branded "Bank of AK"). FastMCP server runs on Hostinger VPS `srv1665337.hstgr.cloud` / `187.124.112.103`, conda env `santander`, Python 3.13, listening on port 80, `streamable-http` transport. Server code lives at `/root/project-x/main.py`.

**Auth plan (deferred — picked up if/when user returns to ChatGPT MCP path):** Use `fastmcp.server.auth.providers.workos.AuthKitProvider` with `authkit_domain` from env var `AUTHKIT_DOMAIN` and `base_url='http://187.124.112.103'`. Requires WorkOS account with Dynamic Client Registration enabled (ChatGPT custom connectors need DCR or a pre-registered OAuth client — they reject API keys, static bearer tokens, mTLS, and client_credentials). `WorkOSProvider` (without "AuthKit") is the wrong class — it needs pre-registered redirect URIs which ChatGPT can't satisfy.

**Why:** Demo audience is students; the ChatGPT custom-connector OAuth dance was the original frame but introduced enough setup friction (WorkOS dashboard config, brand customization, env-var plumbing) that the user pivoted to a simpler email-OTP flow on 2026-05-13.

**How to apply:** If user returns to the ChatGPT-connector path, the AuthKitProvider scaffolding in `/root/project-x/main.py` is the resume point — `auth.py` (the old Auth0/JWKS hand-rolled verifier) is still on disk but unused and can be deleted. If user stays on email-OTP, this memory is historical context, not active guidance.

**Operational rules (mandatory):**
- **Always run the server from the `santander` conda env**, never `base`. `main.py` depends on `fastmcp`, `authlib`, `pydantic` etc. which are only installed in `santander`. `/root/project-x/run_server.sh` enforces this with a hard `CONDA_DEFAULT_ENV == santander` check before `exec python main.py` — do not bypass.
- **Use `/root/project-x/run_server.sh`** for any restart. It (a) detects `cloudflared` already running and reuses its tunnel URL, (b) exports the four pinned env vars (`AUTH0_DOMAIN`, `AUTH0_AUDIENCE=https://project-x-128/mcp`, `RESOURCE_BASE_URL=https://project-x-128`, `MCP_BASE_URL=<live tunnel URL>`), (c) verifies the conda env, (d) `exec`s into python. `./run_server.sh --stop` kills both processes.
- **Cloudflare quick-tunnel URL is stable as long as `cloudflared` keeps running** — restarting only the server keeps the same URL, so the ChatGPT connector keeps working without reconfiguration. Only restart `cloudflared` if you have to.
