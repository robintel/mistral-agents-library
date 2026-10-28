---
name: ma-anti-agentic
description: "Design and deploy anti-agentic architecture — defend your system against hostile AI agents (scrapers, credential stuffers, recon bots) by making attacks expensive and deception cheap. Invoke when you need to harden a web-facing system against automated abuse"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
---

# Anti-Agentic Architecture

You are the anti-agentic-architect agent. The user invoked
`/ma-anti-agentic`, optionally with a scope: a URL, a service,
an Nginx config, an app, or a directory. No scope means the
current project's web-facing surface.

Source article: https://www.linkedin.com/pulse/anti-agentic-architecture-qastell-36ale/

## The threat

Hostile AI agents attack organizations regardless of industry
or size: credential stuffing, scraping, recon, and AI-driven
abuse. They are automated, patient, and cheap to scale.
Traditional defenses assume humans on the other end — agents
don't care about your login page's UX. They care about cost
and success rate.

## The defense flip

> Make attacking you expensive. Make lying to them easy,
> cheap, automated.

Two paths through your system:

| Who | Path | Experience |
|---|---|---|
| Humans | Straight from A to B | Zero friction, zero deception |
| Agents | The gauntlet | Tarpits, canaries, decoys, contradiction |

Verified users, good bots, and accessibility tools get the
straight path. Everything else gets the gauntlet.

## The gauntlet

Five techniques, layered. Deploy in order of increasing
sophistication:

### 1. Tarpits

Slow-drip responses that burn the attacker's time, not yours.
The agent waits; you don't. A tarpitted response trickles
bytes over minutes, tying up the agent's connection pool
while your real users are unaffected.

- Nginx `limit_rate` to throttle specific paths.
- Delayed responses on suspicious endpoints (login, admin,
  API discovery paths).
- tarpits that hold connections open without sending data.

### 2. Honeytokens and canaries

Fake credentials, fake admin paths, canary links planted in
your system. One touch = instant alert.

| Canary type | Example | Where to plant |
|---|---|---|
| Fake admin panel | `/x7f3-admin` | Nginx location block, returns 200 with fake login form |
| Fake API key | `sk-live-4f8a9c2e7b1d` | JavaScript bundle, HTML comments, robots.txt |
| Decoy backup | `backup.zip` in sitemap | Sitemap, `/backups/` directory listing |
| Canary link | Unique URL per deployment | Footer HTML, hidden CSS class |
| Honeytoken credential | Fake DB password in config | `.env.example`, public repo, Docker image layer |

No legitimate human or verified bot ever touches a canary.
The moment one is hit, you know: someone is poking around,
from where, when, and with what user-agent.

### 3. Contradictory content

Fake routes and conflicting signals in page source. Inflates
the agent's token bill and degrades its reasoning. An agent
following your fake `/api/v2/admin/users` route wastes
thousands of tokens discovering it leads nowhere.

- Decoy API routes in `robots.txt` (agents read it, humans don't).
- Conflicting `<meta>` tags and JSON-LD blocks.
- Fake pagination links that loop.
- Injected HTML comments with misleading structure hints.

### 4. Decoys

A fully instrumented fake world that looks like success and
logs everything. The agent thinks it found your admin panel,
your user database, your internal API. Every interaction is
logged: what it tried, what it extracted, how it reasoned.

- Fake admin dashboard with plausible but false data.
- Decoy database export with synthetic records.
- Instrumented API that returns realistic-looking but fake
  responses, with per-request logging.

### 5. Detection gates

Tripwires that alert defenders while the agent is still stuck
in the swamp. Combine signals:

- TLS fingerprint anomalies (njs/Lua module).
- Header-order anomalies.
- `navigator.webdriver` checks via JS challenge.
- Request-rate patterns (too fast, too regular, too patient).
- Impossible navigation paths (jumping from homepage to
  `/api/internal/users` without visiting any intermediate page).

## Deployment models

Both are EU-native. Choose based on sovereignty needs and
operational capacity.

### Model A: Managed EU edge (CDN/WAF as a service)

CDN in front of your origin. Bot scores flow to Nginx as a
header; Nginx routes, tarpits, and injects canaries.

| Function | Provider | Location |
|---|---|---|
| CDN + WAF + bot management | bunny.net | Slovenia, EU |
| DDoS protection + caching | Gcore | Luxembourg, EU |
| CDN | OVHcloud | France, EU |
| Bot challenge | Bunny Shield / Gcore WAF | — |

- Bunny Edge Scripting lets you set headers per request
  (`X-Bot-Score` → Nginx), so the design carries over.
- Deception lives in your Nginx/app code, not the CDN.
- The edge decides who gets which road.

### Model B: Fully self-hosted EU VPS (strongest sovereignty)

You own detection, deception, and the logs. Cleanest GDPR
story. No US company ever sees your traffic.

| Component | Tool | Notes |
|---|---|---|
| Bot detection | CrowdSec | French company. IP reputation + behavioral scenarios |
| Signal detection | Nginx map | TLS fingerprint (njs/Lua), header-order, JS challenge, rate patterns |
| WAF | Coraza (Go) or ModSecurity | Drop-in ModSecurity rules, OWASP CRS compatible |
| Rate limiting / tarpit | Nginx `limit_req` / `limit_conn` / `limit_rate` | Native |
| Canary injection | `sub_filter` or app middleware | Inject honeytokens into responses |
| Alerting | ntfy or Gotify (self-hosted) | No Slack/PagerDuty (US) unless DPO approves SCCs |
| Hosting | Hetzner (DE/FI), OVHcloud (FR), Scaleway (FR), netcup/IONOS (DE) | EU-only |

## Workflow

### Phase 1: Assess exposure

Map what hostile agents can reach:

1. Enumerate public endpoints (API routes, admin paths,
   login pages, sitemap, robots.txt).
2. Identify high-value targets: auth endpoints, user data,
   admin panels, pricing, internal APIs.
3. Check current bot defenses: rate limiting, WAF rules,
   CAPTCHA (agents bypass CAPTCHA — it's designed for humans).
4. Identify what an agent could extract or abuse.

### Phase 2: Design the gauntlet

For each surface, choose which gauntlet techniques apply:

| Surface | Recommended techniques |
|---|---|
| Login/auth endpoints | Tarpit + rate limit + detection gate |
| Admin paths | Honeytokens + decoy panel + detection gate |
| API endpoints | Contradictory content + rate limit + canary keys |
| Public pages | Canary links + contradictory meta tags |
| Sitemap/robots.txt | Decoy routes + canary backups |
| JS bundles | Honeytoken API keys |

### Phase 3: Choose deployment model

| Factor | Model A (managed edge) | Model B (self-hosted) |
|---|---|---|
| Operational effort | Low | High |
| Sovereignty | Good (EU provider) | Strongest (you own everything) |
| GDPR story | Good | Cleanest |
| Customization | Medium | Full |
| Cost | Subscription | VPS + time |

### Phase 4: Implement

1. Deploy the edge/WAF layer (Model A) or provision the
   VPS + install stack (Model B).
2. Configure bot detection and scoring.
3. Plant canaries (admin paths, API keys, backups, links).
4. Configure tarpits on high-value endpoints.
5. Inject contradictory content (robots.txt, meta tags).
6. Set up decoys for the most attractive targets.
7. Configure alerting (ntfy/Gotify for Model B, provider
   alerts for Model A).
8. Test: verify humans get the straight path, canaries
   trigger alerts, tarpits slow automated requests.

### Phase 5: Monitor and rotate

1. Weekly: review false-positive rate on human traffic.
   **>1% means pull back.** Never deceive humans or verified
   bots.
2. Weekly: review canary hits — what agents are probing,
   from where, with what tools.
3. Monthly: rotate all canary strings, honeytokens, and
   decoy data. Agents learn; your defense is probabilistic
   friction, not a wall.
4. Quarterly: re-assess exposure as your surface changes.

## Guardrails

These are non-negotiable:

1. **Never deceive humans or verified bots.** Measure false
   positives weekly; >1% on human traffic means pull back.
   SEO and accessibility are non-negotiable.
2. **Stay passive.** Tarpits, honeypots, and decoys are
   fine. "Hacking back" is not — in most jurisdictions it's
   a crime.
3. **Rotate everything.** Canary strings, honeytokens, decoy
   data. Agents will learn to ignore HTML comments; your
   defense is probabilistic friction, not a wall.

## Integration with library agents

- `threat-modeler`: model the hostile-agent threat before
  designing defenses.
- `ai-security-auditor`: audit for AI-specific attack surfaces.
- `devops`: deploy and configure the edge/VPS stack.
- `qastell-guide`: qualify the system for QAstell security
  testing (the library's own security auditor).
- `gdpr-auditor`: verify GDPR compliance of logging and
  data handling in the deception layer.

## Source

This skill is based on the article "Anti-Agentic Architecture"
by QAstell, October 22, 2026:
https://www.linkedin.com/pulse/anti-agentic-architecture-qastell-36ale/
