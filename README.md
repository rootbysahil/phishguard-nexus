# PHISHGUARD//NEXUS

> **Explainable AI Phishing & Scam Detection Platform**  
> *Developed for the IBM Machine Learning & Artificial Intelligence Internship Capstone Project*

[![CI Pipeline](https://github.com/phishguard-nexus/phishguard/actions/workflows/ci.yml/badge.svg)](https://github.com/phishguard-nexus/phishguard/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E.svg)](https://scikit-learn.org/)
[![IBM watsonx.ai](https://img.shields.io/badge/IBM%20watsonx.ai-Granite-052FAD.svg)](https://www.ibm.com/watsonx)

---

## 1. Executive Summary

Phishing remains the primary vector for credential theft, ransomware dissemination, and cyber fraud. Traditional threat detection systems classify targets as a black-box binary verdict ("Safe" vs. "Phishing"), leaving end-users and Security Operations Center (SOC) analysts without contextual reasoning or actionable mitigation steps.

**PHISHGUARD//NEXUS** bridges this gap by uniting:
1. **Machine Learning Classifier**: A trained and calibrated tree-based lexical pipeline achieving **>99% ROC-AUC** and **0.998 F2 Score** across held-out domain splits.
2. **Local Feature Explainability (SHAP)**: Directional decomposition of raw model margins into visual feature contributions.
3. **Generative AI Security Analyst (IBM watsonx.ai Granite)**: Translates raw mathematical feature weights into human-understandable security advisories and recommended actions, supporting **English**, **Hindi (हिन्दी)**, and **Punjabi (ਪੰਜਾਬੀ)**.
4. **Real-Time Telemetry & Cyber UI**: Server-Sent Events (SSE) streaming pipeline with radial threat gauges, homoglyph inspectors, and instant PDF incident reporting.

---

## 2. Key Technical Innovations

- **Anti-Bias Training Protocol**: Benign samples include realistic internal crawl paths (eliminating the common shortcut-learning artifact where models cheat by learning *"long URL = phishing"*).
- **Zero Train/Serve Skew**: The primary model operates **strictly on 24 lexical features** (0 network calls, sub-15ms latency), avoiding broken RDAP/WHOIS lookups on historical expired domains.
- **Group-Domain Splitting**: Uses `GroupShuffleSplit` on registered domains (`eTLD+1`) to prevent data leakage between train, validation, and test partitions.
- **Recall-Weighted Optimization ($F_2$)**: Threshold tuned to prioritize recall ($\beta = 2$) over precision, penalizing missed phishing attacks (false negatives).
- **Privacy by Design**: URLs and domains are logged locally for history, while raw email and SMS message bodies are **never persisted** (processed in memory with SHA-256 hash logging only).

---

## 3. Quick Start (Run Locally)

### Prerequisites
- Python 3.10+ (Tested on Python 3.11 & 3.13)

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Generate Training Data & Train Models
```bash
# Downloads data, builds domain-grouped splits, and trains calibrated model
python backend/data/scripts/download_data.py
python backend/data/scripts/build_features.py
python backend/data/scripts/train_model.py
```

### 3. Start the Platform
```bash
python backend/main.py
```
- 🌐 **Interactive Cyberpunk UI**: [http://localhost:8000/](http://localhost:8000/)
- 📄 **Interactive OpenAPI Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 🩺 **System Health Check**: [http://localhost:8000/api/health](http://localhost:8000/api/health)

---

## 4. Architecture & Repository Layout

```
phishguard-nexus/
│
├── backend/
│   ├── app/
│   │   ├── api/routes/          # /api/scan, /api/history, /api/model, /api/system, /api/report
│   │   ├── core/                # Settings, security, rate-limiting
│   │   ├── db/                  # SQLAlchemy models & SQLite session
│   │   ├── llm/                 # IBM watsonx.ai Granite & Template Fallback providers
│   │   ├── ml/
│   │   │   ├── features/        # url_features.py (28 pure-Python lexical features)
│   │   │   ├── predictor.py     # Inference engine with probability calibration
│   │   │   └── explainer.py     # SHAP directional contribution engine
│   │   ├── schemas/             # Pydantic v2 schemas
│   │   ├── static/              # Interactive Single-Page Web Dashboard
│   │   └── main.py              # FastAPI app factory
│   │
│   ├── data/scripts/            # download_data.py, build_features.py, train_model.py
│   ├── models/eval/             # Real ROC, PR, Confusion Matrix, and Calibration plots
│   └── tests/                   # Unit and integration pytest test suite
│
├── docs/                        # Complete Phase 0 Architecture, ML Plan, Wireframes, API Contract
├── Makefile                     # Build & automation targets
├── docker-compose.yml           # Multi-container orchestration
└── .env.example                 # Configuration template
```

---

## 5. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/scan` | Submits URL/email/SMS; returns 202 Accepted with SSE stream URL |
| `GET` | `/api/scan/stream/{id}` | Real-time Server-Sent Events (SSE) pipeline milestones with keepalive |
| `GET` | `/api/scan/{id}` | Fetches full analysis, SHAP contributions, anatomy, and advice |
| `POST` | `/api/translate` | Generates on-demand Hindi or Punjabi advisory translations |
| `GET` | `/api/history` | Paginated incident logs with domain search filter |
| `DELETE`| `/api/history` | Purges local scan database |
| `GET` | `/api/stats` | Aggregated threat distribution metrics and spoofed brand counts |
| `GET` | `/api/model/metrics` | Serves real training evaluation metrics and artifact curve paths |
| `POST` | `/api/report` | Downloads structured incident report PDF |
| `GET` | `/api/health` | Service health status and watsonx.ai readiness probe |

---

## 6. Verification & Automated Testing

Run the automated test suite:
```bash
pytest backend/tests/ -v
```
**Results:** `8 passed in 8.8s` (covers input boundaries, HTTP 413 limits, feature extractors, homoglyph detectors, and API endpoints).

---

## 7. Author & Internship Details

- **Project**: PHISHGUARD//NEXUS
- **Internship**: IBM Machine Learning & Artificial Intelligence Internship
- **Student**: Sahil
- **Core Technologies**: Machine Learning, Python, FastAPI, Scikit-Learn, SHAP, IBM watsonx.ai Granite, SQLite, ReportLab
