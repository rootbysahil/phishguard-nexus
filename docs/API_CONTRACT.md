# PHISHGUARD//NEXUS — API Contract

> Phase 0 planning document.
> All schemas expressed as Pydantic v2 models (Python type annotations).
> Auto-generated OpenAPI docs available at `GET /docs` and `GET /redoc`.

---

## Base URL

```
http://localhost:8000/api
```

---

## Global Constraints & Limits

| Constraint | Value | Error Code |
|---|---|---|
| Max URL length | 2,048 characters | HTTP 413 (Payload Too Large) |
| Max Email / SMS text | 50 KB | HTTP 413 (Payload Too Large) |
| Rate limit (`/api/scan`) | 30 requests / min / IP | HTTP 429 (Too Many Requests) |
| Rate limit (other endpoints) | 120 requests / min / IP | HTTP 429 (Too Many Requests) |
| SSE Keepalive interval | 5 seconds (`: ping\n\n`) | — |
| CORS allowed origins | Configured via `CORS_ORIGINS` env var | HTTP 403 |

---

## 1. POST /api/scan

Submits content for asynchronous analysis. Returns immediately with HTTP 202 Accepted containing the `scan_id` and the SSE streaming endpoint URL. CPU-bound inference runs in a backend thread pool.

### Request Body

```json
{
  "type": "url",
  "content": "http://paypa1.secure-verify.net/account/login?token=abc"
}
```

*Fields:*
- `type`: `url` | `email` | `sms` (required)
- `content`: string (required; max 2,048 chars for `url`, max 50 KB for `email`/`sms`)

### Response 202 (Accepted)

```json
{
  "scan_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "stream_url": "/api/scan/stream/550e8400-e29b-41d4-a716-446655440000"
}
```

### Error Responses

| Code | When |
|---|---|
| 413 | Content exceeds payload limits (>2,048 chars for URL, >50 KB for text) |
| 422 | Schema validation failure (invalid type enum, empty content) |
| 429 | Rate limit exceeded |

---

## 2. GET /api/scan/stream/{scan_id}

Server-Sent Events (SSE) progress stream. Connect via EventSource. Closed by server after the terminal `done` event.

### SSE Event Stream Shape

```
: ping

data: {"stage":"parse","pct":15,"detail":"Parsed domain: secure-verify.net"}

data: {"stage":"features","pct":40,"detail":"Extracted 28 lexical features"}

data: {"stage":"inference","pct":80,"detail":"Calibrated LightGBM inference complete"}

data: {"stage":"explain","pct":95,"detail":"SHAP values & watsonx explanation generated"}

data: {"stage":"done","pct":100,"scan_id":"550e8400-e29b-41d4-a716-446655440000"}
```

*Notes:*
- Comment `: ping` keepalives are emitted every 5s to keep connections alive.
- Stage sequence: `parse` → `features` → `reputation` (optional) → `inference` → `explain` → `done`.
- Event queues are strictly evicted from server memory upon sending `done` or client disconnect.

---

## 3. GET /api/scan/{scan_id}

Fetches the complete result for a completed scan. Used when routing directly to `/scan/{id}` or on page refresh.

### Response 200

```json
{
  "scan_id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "url",
  "target": "paypa1.secure-verify.net",
  "content_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "verdict": "PHISHING",
  "probability": 0.87,
  "risk_level": 9,
  "features": {
    "url_length": 58,
    "ip_in_host": 0,
    "shannon_entropy": 3.84,
    "typosquat_distance": 1,
    "brand_kw_in_subdomain": 1,
    "https_present": 0
  },
  "shap_contributions": [
    { "feature": "brand_kw_in_subdomain", "value": 0.42, "direction": "phishing" },
    { "feature": "typosquat_distance",    "value": 0.31, "direction": "phishing" },
    { "feature": "https_present",         "value": 0.18, "direction": "phishing" },
    { "feature": "dot_count",             "value": -0.04, "direction": "safe" }
  ],
  "red_flags": [
    "Brand keyword 'paypal' impersonated in subdomain",
    "Homoglyph detected: 'l' replaced with '1' in 'paypa1'",
    "Insecure HTTP protocol used"
  ],
  "url_anatomy": {
    "protocol": "http",
    "subdomain": "paypa1",
    "domain": "secure-verify",
    "tld": ".net",
    "path": "/account/login",
    "query": "?token=abc",
    "suspicious_segments": ["subdomain", "domain"],
    "homoglyph_detail": {
      "detected": true,
      "original": "paypal",
      "found": "paypa1",
      "swapped_pos": 5,
      "swapped_char": "1"
    },
    "typosquat": {
      "detected": true,
      "target_brand": "paypal.com",
      "edit_distance": 1
    }
  },
  "explanation": {
    "en": "This URL mimics PayPal using a homoglyph substitution ('1' for 'l') in the subdomain to deceive users into credential entry.",
    "why_flagged": "Subdomain homoglyph and brand impersonation combined with unencrypted HTTP transport.",
    "what_to_do": "Do not enter credentials. Report to cybercrime.gov.in (Helpline 1930) or APWG (reportphishing@apwg.org).",
    "powered_by": "watsonx"
  },
  "inference_latency_ms": 14,
  "created_at": "2024-11-01T12:34:56Z"
}
```

*Notes on fields:*
- `risk_level`: Integer on a scale of `0` to `10` calculated as `round(probability * 10)`.
- `shap_contributions`: `value` is signed log-odds contribution; `direction` is `"phishing"` or `"safe"`.
- `explanation`: Serves English by default. Hindi/Punjabi are generated on-demand via `POST /api/translate`.

### Error Responses

| Code | When |
|---|---|
| 404 | `scan_id` does not exist |
| 422 | Invalid UUID format |

---

## 4. POST /api/translate

Generates an on-demand translation of an advisory scan explanation.

### Request Body

```json
{
  "scan_id": "550e8400-e29b-41d4-a716-446655440000",
  "target_language": "hi"
}
```

*Fields:*
- `scan_id`: UUID (required)
- `target_language`: `hi` | `pa` (required; Hindi or Punjabi)

### Response 200

```json
{
  "scan_id": "550e8400-e29b-41d4-a716-446655440000",
  "language": "hi",
  "translated_explanation": "यह URL सबडोमेन में होमोग्लिफ़ का उपयोग करके PayPal की नकल करता है ताकि उपयोगकर्ताओं को धोखा देकर क्रेडेंशियल दर्ज कराए जा सकें।",
  "what_to_do": "अपने क्रेडेंशियल्स दर्ज न करें। cybercrime.gov.in (हेल्पलाइन 1930) पर रिपोर्ट करें।"
}
```

---

## 5. GET /api/history

Returns paginated scan history.

### Query Parameters

| Param | Type | Default | Description |
|---|---|---|---|
| `page` | int | 1 | Page number |
| `limit` | int | 20 | Items per page (max 100) |
| `verdict` | string | null | Filter: `SAFE`, `SUSPICIOUS`, `PHISHING` |
| `type` | string | null | Filter: `url`, `email`, `sms` |
| `q` | string | null | Search filter across stored **target domain/URL** and red flags |
| `sort` | string | `created_at:desc` | Sort field and order |

### Response 200

```json
{
  "total": 42,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "scan_id": "550e8400-e29b-41d4-a716-446655440000",
      "target": "paypa1.secure-verify.net",
      "type": "url",
      "verdict": "PHISHING",
      "probability": 0.87,
      "risk_level": 9,
      "red_flags": ["Brand keyword 'paypal' impersonated in subdomain"],
      "created_at": "2024-11-01T12:34:56Z"
    }
  ]
}
```

---

## 6. DELETE /api/history

Purges all stored scan records from the local SQLite database.

### Response 200

```json
{
  "status": "success",
  "deleted_count": 42,
  "message": "All local scan records purged."
}
```

---

## 7. GET /api/stats

Returns aggregated summary statistics for the dashboard.

### Response 200

```json
{
  "total_scans": 42,
  "phishing_count": 14,
  "suspicious_count": 6,
  "safe_count": 22,
  "verdict_distribution": {
    "PHISHING": 0.333,
    "SUSPICIOUS": 0.143,
    "SAFE": 0.524
  },
  "top_spoofed_brands": [
    { "brand": "paypal", "count": 8 },
    { "brand": "microsoft", "count": 4 }
  ],
  "detections_over_time": [
    { "date": "2024-11-01", "phishing": 2, "suspicious": 1, "safe": 5 }
  ],
  "scan_type_breakdown": {
    "url": 32,
    "email": 6,
    "sms": 4
  }
}
```

---

## 8. GET /api/config

Returns dynamic backend settings, classification thresholds, and reporting configuration.

### Response 200

```json
{
  "threshold_safe": 0.35,
  "threshold_suspicious": 0.70,
  "reporting_region": "IN",
  "reporting_authorities": {
    "primary_portal": "https://cybercrime.gov.in",
    "helpline": "1930",
    "global_portal": "reportphishing@apwg.org"
  },
  "features_enabled": {
    "host_features": false,
    "distilbert": false
  }
}
```

---

## 9. GET /api/health

Health check endpoint used by the frontend boot sequence and Docker health checks.

### Response 200

```json
{
  "status": "ok",
  "version": "1.0.0",
  "components": {
    "database": "connected",
    "ml_model": "loaded",
    "explainer": "ready",
    "watsonx_ai": "ready"
  }
}
```

*(Note: `watsonx_ai` returns `"offline"` if API credentials are invalid or unreachable; the backend falls back gracefully to template explanation).*

---

## 10. GET /api/model/metrics

Returns model evaluation metrics from `models/eval/metrics.json`.
**All metrics default strictly to `null` until populated by `make evaluate` in Phase 3.** No fabricated values.

### Response 200

```json
{
  "model_name": "LightGBM",
  "trained_at": null,
  "dataset_split": {
    "train": null,
    "val": null,
    "test": null
  },
  "threshold": null,
  "precision": null,
  "recall": null,
  "f1": null,
  "f2": null,
  "roc_auc": null,
  "pr_auc": null,
  "ece": null,
  "inference_latency_ms": {
    "p50": null,
    "p95": null
  },
  "confusion_matrix": null,
  "plot_paths": {
    "roc_curve": "/static/eval/roc_curve.png",
    "pr_curve": "/static/eval/pr_curve.png",
    "confusion_matrix": "/static/eval/confusion_matrix.png",
    "calibration_curve": "/static/eval/calibration_curve.png",
    "shap_global": "/static/eval/shap_global.png"
  },
  "fresh_url_eval": {
    "f2": null,
    "roc_auc": null,
    "sample_size": null,
    "note": "Evaluated on held-out post-cutoff feed"
  }
}
```

---

## 11. POST /api/report

Generates a downloadable PDF incident report for a specific scan.

### Request Body

```json
{
  "scan_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Response 200

```
Content-Type: application/pdf
Content-Disposition: attachment; filename="phishguard-report-550e8400-e29b-41d4-a716-446655440000.pdf"

<binary PDF stream>
```

---

## 12. Standard Error Envelope

All HTTP 4xx and 5xx errors return a uniform structure:

```json
{
  "error": {
    "code": "PAYLOAD_TOO_LARGE",
    "message": "Input content length exceeds the 2,048 character limit for URLs.",
    "detail": null
  }
}
```

---

## 13. Privacy & Data Handling Guarantees

- **URL Scans**: The domain name and URL tokens are stored in the local SQLite database to populate user scan history and search.
- **Email & SMS Scans**: Raw text content is **never persisted** to disk or database. Extracted features and verdict are computed in memory, and the raw text is immediately discarded. A SHA-256 hash is retained strictly for duplicate detection.
