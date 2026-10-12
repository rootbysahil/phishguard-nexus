# PHISHGUARD//NEXUS — UI Wireframes & Screen Descriptions

> Phase 0 planning document.
> Screen-by-screen specifications and user interaction states. Visual tokens in Section 1.

---

## 1. Design Identity

### Color Palette (design tokens in `frontend/src/lib/theme.ts`)

| Token | Hex | Usage |
|---|---|---|
| `color.bg` | `#05060A` | Page background |
| `color.surface` | `#0D0F18` | Card / panel background |
| `color.border` | `#1A2040` | Default border |
| `color.cyan` | `#00F0FF` | Primary accent, links, active states |
| `color.magenta` | `#FF2BD6` | Secondary accent, highlights |
| `color.safe` | `#39FF14` | SAFE verdict, positive indicators |
| `color.suspicious` | `#FFB800` | SUSPICIOUS verdict, warnings |
| `color.danger` | `#FF2E4D` | PHISHING verdict, critical alerts |
| `color.text` | `#E0E6FF` | Primary text |
| `color.muted` | `#6B7BA4` | Secondary / hint text |

### Typography

| Role | Font |
|---|---|
| Headings, logo | Orbitron (Google Fonts) |
| UI labels, body | Rajdhani |
| Terminal output, code, hashes | JetBrains Mono |

### Visual Effects (all togglable in Settings — "Reduced Effects" mode)

- **Scanlines overlay**: repeating horizontal lines at 2px pitch, 6% opacity
- **Vignette**: radial gradient darkening edges
- **Animated grid background**: faint perspective grid that slowly drifts
- **Glitch text effect**: periodic horizontal jitter on headings (Framer Motion)
- **HUD corner brackets**: `┌ ┐ └ ┘` styled corners on key cards (CSS)
- **Neon glow borders**: `box-shadow` with the relevant accent color
- **Glassmorphism panels**: `backdrop-filter: blur(12px)` + semi-transparent bg
- **Screen shake**: brief `transform: translate()` animation on PHISHING verdict

---

## 2. Screen 0 — Boot Sequence

**Trigger:** First page load per session. `sessionStorage.bootPlayed` prevents replay.

**Layout:** Full-screen black overlay above the main app.

**Animation sequence (skippable by pressing any key or clicking):**

```text
[JetBrains Mono, green text, typing animation at ~60 chars/sec]

PHISHGUARD//NEXUS v1.0.0
INITIALIZING NEURAL SHIELD...

> Loading threat intelligence model........... [OK]
> Calibrating probability estimator........... [OK]
> Connecting to IBM watsonx.ai Granite......... [READY / OFFLINE]
> Mounting explainability engine............... [OK]
> Building URL anatomy parser.................. [OK]

ALL SYSTEMS NOMINAL.
THREAT DETECTION ACTIVE.

[PRESS ANY KEY TO ENTER — or auto-skip in 3s]
```

The `[READY / OFFLINE]` status for watsonx is driven by a real API health ping (`GET /api/health`).
The overlay fades out with a CRT-power-off animation (brief white flash, then collapse).

---

## 3. Screen 1 — Scan Console (Main / Hero)

**Route:** `/`  
**Purpose:** Primary entry point. Users submit URL, email, or SMS for analysis.

```text
┌─────────────────────────────────────────────────────────────────────┐
│  PHISHGUARD//NEXUS  ░░░░░░░░░░░░░░░░░░░░░  [Ctrl+K] [⚙] [🔇] [?]  │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  ┌─ SCAN CONSOLE ──────────────────────────────────────────────┐   │
│  │  [  URL  ]  [ EMAIL ]  [  SMS  ]                            │   │
│  │                                                             │   │
│  │  ┌──────────────────────────────────────────────────────┐  │   │
│  │  │ > _                                                  │  │   │
│  │  │   Paste a URL, email body, or SMS text here          │  │   │
│  │  │   Drag & drop a .eml file (client-parsed, max 5MB)   │  │   │
│  │  └──────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  │  [▶ ANALYZE THREAT]    [DEMO: Phishing] [DEMO: Safe]       │   │
│  │  ⚠ Email/SMS body is never stored — URLs/domains saved in local history │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Recent Scans: [paypal.secure-login.xyz — PHISHING] ...            │
└─────────────────────────────────────────────────────────────────────┘
```

**Interaction notes:**
- Tab switches input mode; the placeholder text changes per mode.
- Drag-and-drop parses `.eml` files strictly client-side using a browser MIME parser library (e.g. `mailparser` / `eml-format`) with a 5 MB file size limit. The raw `.eml` file is never sent to the backend. Extracted plain text / extracted links are populated into the input area.
- "DEMO" buttons load hardcoded sample test vectors labeled explicitly as demo cases.
- Audio effects are opt-in (muted by default; toggled in Settings).
- `[ANALYZE THREAT]` transitions to a glowing cyber spinner upon submit.

---

## 4. Screen 1b — Live Scan Pipeline (inline, below console)

**Trigger:** Displays immediately when analysis starts via Server-Sent Events (SSE).

```text
┌─ SCAN PIPELINE ─────────────────────────────────────────────────────┐
│                                                                     │
│  [ PARSE ] ──── [ FEATURES ] ──── [ REPUTATION ] ──── [ INFER ]   │
│     ✓                ✓                  ●                  ○        │
│                                         ▲                           │
│                                "Evaluating domain lexical tokens…"  │
│                                                                     │
│  ████████████████████░░░░░░░░░░  60%                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Interaction notes:**
- Stage nodes illuminate with cyan neon glow as SSE messages stream from `GET /api/scan/stream/{id}`.
- SSE events include `stage`, `pct`, and `detail`. Progress bar advances using genuine `pct` values.
- Keepalive SSE heartbeats (`: ping`) occur every 5 seconds to prevent network timeouts.

---

## 5. Screen 2 — Scan Result

**Route:** `/scan/{scan_id}`  
**Layout:** Two-column desktop layout (Threat Gauge & Anatomy left; Explainability & AI Analyst right); responsive single-column layout on mobile.

### 5a. Threat Gauge (top left)

```text
            ╭──────────────────────╮
           ╱  ░░░░░░░░░░░░░░░░░░░  ╲
          │    ░ THREAT LEVEL  ░    │
          │         87%             │
          │    ██████████████░░░    │
          │                         │
          │  ╔═══════════════════╗  │
          │  ║   P H I S H I N G ║  │
          │  ╚═══════════════════╝  │
           ╲                       ╱
            ╰───────────────────────╯
```

**Animation & Logic:**
- Arc sweeps from 0% to `calibrated_probability * 100%` over 1.2 s using Framer Motion.
- **Dynamic Thresholds:** Color tiers (green → amber → red) are driven by backend thresholds received from `/api/config` (`threshold_safe` and `threshold_suspicious`), **never hardcoded in UI code**.
- On PHISHING verdict: brief screen shake (4px jitter for 200 ms) and neon red border pulse.
- Rubber-stamp animation displays the final verdict banner (SAFE, SUSPICIOUS, or PHISHING).

### 5b. URL Anatomy View (top right, URL scans only)

```text
  https  ://  paypa1.secure  .  login  .com  /verify/account  ?token=abc
  ┌────┐      ┌────────────┐    ┌─────┐┌───┐
  │safe│      │ ⚠ SUSPECT │    │safe ││safe│
  └────┘      └────────────┘    └─────┘└───┘
                    │
                    └─ Homoglyph detected: 'l' → '1'
                       Typosquat distance: 1 from 'paypal.com'
```

**Interaction notes:**
- Segment tokens are broken down visually: Scheme, Subdomain, Domain, TLD, Path, Query.
- Badges indicate risk status: Safe (dim border), Suspicious (amber glow), Danger (red glow).
- Hovering reveals detailed detection reason.
- For Email and SMS scans, this section is replaced by an **Extracted Links & Intent Inspector**.

### 5c. Explainability Panel (bottom left)

```text
  FEATURE INFLUENCE (SHAP EXPLANATION)
  ─────────────────────────────────────────────────────────────
  brand_kw_in_subdomain  ████████████████  +0.42  → PHISHING
  typosquat_distance     ████████████      +0.31  → PHISHING
  entropy_subdomain      ████████          +0.18  → PHISHING
  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ (baseline) ─ ─ ─ ─
  https_present          ████              -0.12  → SAFE
  valid_tld              ██                -0.08  → SAFE
  ─────────────────────────────────────────────────────────────
  * SHAP values reflect raw model score contributions before calibration.
```

**Interaction notes:**
- Positive SHAP contributions (pushing toward phishing) render in magenta/red bars.
- Negative SHAP contributions (pushing toward safe) render in cyan/green bars.
- Hovering shows clear feature documentation (e.g., *"Subdomain contains popular brand name not belonging to registrant"*).
- Clear footnote explains that SHAP values decompose the raw model margin score, while the gauge displays calibrated probability.

### 5d. AI Analyst Panel (bottom right)

```text
  ┌─ AI SECURITY ANALYST ───────────────── Powered by IBM watsonx.ai ─┐
  │                                                                    │
  │  Language: [ English (Active) ] [ हिंदी (Translate) ] [ ਪੰਜਾਬੀ ]   │
  │                                                                    │
  │  "Analysis indicates this URL impersonates PayPal services.        │
  │   The attacker uses a homoglyph substitution ('1' for 'l') in      │
  │   the subdomain paypa1 to deceive users into sharing credentials." │
  │                                                                    │
  │  WHY WAS THIS FLAGGED?                                             │
  │  ▸ High lexical risk score, unverified domain origin, brand mismatch│
  │                                                                    │
  │  WHAT SHOULD I DO NOW?                                             │
  │  ▸ Region: [ India (Default) ▼ ]                                   │
  │    1. Do NOT click or submit credentials.                          │
  │    2. Report incident to the National Cyber Crime Portal:          │
  │       cybercrime.gov.in or dial national helpline 1930.            │
  │    3. Global: Report phishing links to reportphishing@apwg.org.    │
  │                                                                    │
  │  ⚠ AI explanations are advisory. Always verify critical indicators.│
  └────────────────────────────────────────────────────────────────────┘
```

**Interaction notes:**
- **On-Demand Translation Flow**: Initial explanation streams in **English first**. Hindi (`हिं`) and Punjabi (`ਪੰਜ`) translations are **not** bundled initially; clicking a language pill triggers an on-demand request to `POST /api/translate`, displaying a localized cyber-skeleton loader followed by a client-side typewriter animation upon receipt.
- "WHY WAS THIS FLAGGED?" and "WHAT SHOULD I DO NOW?" sections are collapsible accordions.
- **Configurable Incident Reporting**: Default reporting instructions highlight verified Indian resources (**cybercrime.gov.in** and national helpline **1930**), with a dropdown toggle for Global reporting (**APWG** `reportphishing@apwg.org`).
- IBM watsonx.ai badge shows "Offline Mode — Rule Template Fallback" if the watsonx service is unreachable.

### 5e. Report Export

```text
  [⬇ EXPORT INCIDENT REPORT PDF]
```

Button triggers `POST /api/report` to download a structured, time-stamped incident report PDF.

---

## 6. Screen 3 — Global Threat Map

**Route:** `/map`  
**Component:** `ThreatMap` (Three.js / React Three Fiber)

```text
  ┌─ GLOBAL THREAT INTELLIGENCE RADAR ──────────────────────────────┐
  │                                                                  │
  │               ⊙  [Interactive 3D Threat Radar]                  │
  │          ╱╲       Rotatable cyber globe                         │
  │         ╱  ╲      Target threat nodes & hosting clusters        │
  │        ╱ ●──╲───────────────────────●                           │
  │       ╱      ╲    Origin Radar Anchor → Target Threat Host      │
  │      ╱        ╲                                                  │
  │                                                                  │
  │  [DEMO / KNOWN THREAT NODES — No client IP geocoded]            │
  │  Top Host Origins: AS13335 (Cloudflare), AS16276 (OVH), etc.    │
  └──────────────────────────────────────────────────────────────────┘
```

**Interaction & Privacy Notes:**
- **Zero Client Geolocation**: The application **does not** collect or send the user's IP address to any external geolocation service. The origin node uses a fixed stylized defense hub / radar coordinate anchor.
- Scanned host coordinates are resolved server-side from public domain DNS records only.
- "Reduced Effects" mode substitutes the 3D WebGL globe with an interactive 2D SVG canvas.

---

## 7. Screen 4 — Dashboard & Incident Log

**Route:** `/dashboard`

```text
┌─────────────────────────────────────────────────────────────────────┐
│  THREAT COMMAND CENTER — DASHBOARD                                  │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ TOTAL SCANS  │  │  THREATS     │  │  CLEAN RATE  │             │
│  │    [ — ]     │  │    [ — ]     │  │    [ —% ]    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                     │
│  [Verdict Distribution]       [Scans Over Time]                     │
│                                                                     │
│  TOP SUSPICIOUS DOMAINS DETECTED                                    │
│  • paypa1-verification.com                                          │
│  • secure-banking-update.net                                        │
│                                                                     │
│  ─────────────────── SCAN HISTORY ──────────────────────────────── │
│  [Filter: ALL ▼] [Type: ALL ▼] [🔍 Search domain…] [⬇ Export CSV]   │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ # │ Target Domain/Host    │ Type │ Verdict    │ Score │ Time │  │
│  │ 1 │ paypa1-verify.com     │ URL  │ PHISHING   │ 0.94  │ 2m   │  │
│  │ 2 │ secure-login-node.xyz │ URL  │ SUSPICIOUS │ 0.61  │ 12m  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  Note: Raw email and SMS message bodies are never stored in history.│
└─────────────────────────────────────────────────────────────────────┘
```

**Interaction notes:**
- Search bar queries stored domain names (not opaque hashes).
- Clear audit statement: URLs/domains are retained locally for history; raw email and SMS texts are discarded immediately after memory inference.

---

## 8. Screen 5 — Model Lab (Evaluation & Transparency)

**Route:** `/model-lab`  
**Purpose:** Displays verified model evaluation artifacts generated during Phase 3.

```text
┌─────────────────────────────────────────────────────────────────────┐
│  MODEL LAB — Performance & Evaluation Artifacts                     │
│                                                                     │
│  ┌─ COMPARATIVE BENCHMARK (Hold-Out Test Split) ──────────────────┐ │
│  │ Model Architecture │ F2 Score │ ROC-AUC │ PR-AUC │ Latency p95 │ │
│  │ LightGBM (Primary) │ —        │ —       │ —      │ — ms        │ │
│  │ XGBoost            │ —        │ —       │ —      │ — ms        │ │
│  │ Random Forest      │ —        │ —       │ —      │ — ms        │ │
│  │ Logistic Regression│ —        │ —       │ —      │ — ms        │ │
│  └────────────────────────────────────────────────────────────────┘ │
│  * Metrics populated directly from Phase 3 evaluation run artifacts.│
│                                                                     │
│  [ROC Curve Plot]            [Precision-Recall Curve]              │
│  [Calibration Curve]         [Global Feature Importance]           │
│                                                                     │
│  ─────────────────────────────────────────────────────────────────  │
│  FRESH-URL EVALUATION (Out-of-Distribution Feed Split)              │
│  Status: [Run `make evaluate` to populate fresh evaluation metrics] │
│                                                                     │
│  [⬇ VIEW MODEL_CARD.md]   [⬇ VIEW DATASETS.md]                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Transparency Rules:**
- **Strictly No Invented Numbers**: Every cell in the benchmark table defaults to `—` or `XX.XX` until populated by real outputs from `make evaluate`.
- If evaluation plots do not exist in `/static/eval/`, placeholder cards instruct the user to run the evaluation pipeline.

---

## 9. Screen 6 — Settings

**Route:** `/settings`

```text
  SYSTEM CONFIGURATION & PRIVACY
  ────────────────────────────────────────────────────────
  Visual Intensity          [━━━━━━━━●──] 80%
  Reduced Effects Mode      [ OFF / ON ]  (disables scanlines, 3D globe)
  Sound Feedback            [ OFF / ON ]  (muted by default)
  Default AI Language       [ English ▼ ]
  Reporting Region          [ India (1930 / cybercrime.gov.in) ▼ ]
  ────────────────────────────────────────────────────────
  Data Management & Privacy
  ────────────────────────────────────────────────────────
  Stored Data: Domain search records, verdict logs.
  Privacy Guarantee: Raw email & SMS text bodies are never stored.
  [PURGE SCAN HISTORY]  (Deletes all local records in SQLite)
```

---

## 10. Command Palette (Ctrl+K)

Quick navigation overlay powered by `cmdk`.

```text
  ╔═══════════════════════════════════════╗
  ║  > Search command or route…           ║
  ║  ─────────────────────────────────    ║
  ║  ⚡  Scan URL                          ║
  ║  ✉   Scan Email Text                  ║
  ║  💬  Scan SMS Message                 ║
  ║  📊  Go to Threat Dashboard           ║
  ║  🔬  Open Model Lab                   ║
  ║  ⚙   Open Settings                    ║
  ║  📄  Export Recent Incident Report    ║
  ╚═══════════════════════════════════════╝
```

---

## 11. Empty, Error, and Offline Fallbacks

| View | Empty State | Error State | Offline / Degraded State |
|---|---|---|---|
| **Dashboard** | "No recent scans. Analyze a target in the console." | "Failed to load scan records." | "Offline mode: Showing cached local history." |
| **Threat Map** | "Radar initialized. Scan a target to view host nodes." | "WebGL canvas failed to load. Switch to 2D view." | Renders static 2D vector fallback. |
| **Model Lab** | "Evaluation artifacts pending. Run `make evaluate`." | "Failed to load evaluation figures." | "Evaluation metrics currently unavailable." |
| **AI Analyst** | "Awaiting scan input." | "watsonx service timeout. Using rule-based explanation." | Displays offline rule-based explanation badge. |

---

## 12. Accessibility & Performance Specifications

| Standard | Implementation |
|---|---|
| **Prefers-reduced-motion** | CSS media queries halt floating grid drifts and bypass the 3D canvas. |
| **Color Contrast** | High-contrast neon accents comply with WCAG AA against `#05060A` background. |
| **Keyboard Navigation** | Complete tab focus indexing with visible focus rings across all inputs. |
| **Lazy Loading** | 3D Threat Radar canvas loaded dynamically via `import()` chunking. |
| **Privacy by Design** | Strict separation: URL/domain logged for scan history; message bodies never persisted. |
