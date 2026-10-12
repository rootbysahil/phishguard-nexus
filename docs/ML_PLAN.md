# PHISHGUARD//NEXUS — Data & ML Plan

> Phase 0 planning document.
> Machine learning architecture, feature engineering, and evaluation protocol.

---

## 1. Data Sources & Transparency

All sources are publicly accessible and licensed for research. Full license terms are detailed in `docs/DATASETS.md`.

| # | Source | Content | Modality | License / Terms |
|---|---|---|---|---|
| 1 | PhishTank Verified Feed (CSV) | Verified active phishing URLs | Raw URLs | CC BY-SA 2.5 |
| 2 | OpenPhish Community Feed (TXT) | Active phishing URLs | Raw URLs | Research / Non-commercial |
| 3 | Kaggle Malicious & Phishing URLs | 500k+ labelled URLs (benign & malicious) | Raw URLs | ODbL / Open Data |
| 4 | Tranco Top-1M List + Internal Paths | Benign base domains + sampled deep paths | Raw URLs | CC BY 4.0 |
| 5 | Nazario Phishing Email Corpus | Real-world credential phishing emails | Email text | Public Domain / Research |
| 6 | SpamAssassin Public Corpus | Ham and spam email reference | Email text | Apache 2.0 |
| 7 | UCI SMS Spam Collection | Mobile spam and legitimate SMS text | SMS text | CC BY 4.0 |

> **Dataset Integrity Note:** The legacy UCI "Phishing Websites" dataset contains only 30 pre-computed categorical attributes (-1, 0, 1) and does not provide raw URL strings. It is excluded from the URL lexical pipeline to ensure all features are extracted end-to-end by our own feature engineering code.

### 1.1 Mitigating Dataset Bias & Path-Length Artifacts
Benign feeds (e.g. Tranco) predominantly consist of root domains (`domain.com`), whereas phishing feeds consist of deep paths (`domain.com/secure/login.php`). To prevent the model from learning the superficial shortcut *"deep path = phishing"*:
1. **Realistic Benign Deep Paths**: Benign base domains are paired with real internal crawl paths sampled from open sitemaps and the Kaggle benign URL corpus.
2. **Length/Path Ablation Study**: We train and report a secondary ablation model with all length, dot-count, and path-depth features removed, validating that lexical tokens and entropy carry authentic discriminative signal.

---

## 2. Feature Engineering Pipeline

### 2.1 Primary Model: URL Lexical Features (Deterministic; 0 Network Calls)
The primary production model operates **strictly on lexical and string-level characteristics**, ensuring sub-15ms inference latency and zero train/serve skew from dead domains.

| Feature Name | Description | Rationale |
|---|---|---|
| `url_length` | Total character length of URL | Phishing URLs often use lengthy obfuscation |
| `digit_ratio` | Ratio of digits to total length | Random hash generation / session token masquerade |
| `dot_count` | Number of `.` characters | Excessive subdomains and misleading host names |
| `hyphen_count` | Number of `-` characters | Common in deceptive brand pairings (`paypal-verify`) |
| `at_symbol_present` | Binary: `@` in URL | RFC 3986 trick to ignore preceding credentials |
| `subdomain_depth` | Count of labels preceding registered domain | Deep subdomain nesting (`login.secure.bank.com.xyz`) |
| `path_depth` | Count of `/`-delimited path segments | Deep directory hierarchy |
| `shannon_entropy` | Entropy of the domain label | Detects algorithmically generated domains (DGA) |
| `ip_in_host` | Binary: host is a bare IPv4 / IPv6 address | Phishing hosted on unmapped IP addresses |
| `punycode_detected` | Binary: presence of `xn--` prefix | IDN homograph attack indicator |
| `homoglyph_detected` | Binary: character substitutions (e.g., `1` for `l`) | Typosquatting and spoofing of popular brands |
| `brand_in_subdomain` | Binary: Top-100 brand keyword in subdomain | Subdomain impersonation |
| `typosquat_distance` | Min Levenshtein distance to Top-100 brand list | Brand imitation detection |
| `suspicious_tld` | Binary: TLD belongs to high-abuse registrar list | High-risk TLD filtering |
| `https_present` | Binary: URL scheme begins with HTTPS | Phishing increasingly uses free TLS certs |

### 2.2 Optional Auxiliary Pipeline: Host & Network Intelligence
To eliminate train/serve skew, host-level features are **never combined into the primary lexical model**. They are computed asynchronously via an optional enrichment service only when network lookups are enabled:
- `domain_age_days`: RDAP query (flags domains created < 14 days ago).
- `dns_a_record_count`: DNS resolver query count.
- `asn_country_code`: IP BGP lookup.

### 2.3 Email & SMS Text Features (Scam/Phishing Language Signals)
- **Lexical Text Pipeline**: TF-IDF vectorizer (unigrams + bigrams, top-5,000 terms) fitted on training split.
- **Security Intent Heuristics**:
  - `urgency_count`: Count of urgency triggers ("suspended", "verify within 24h", "immediate action").
  - `credential_request_count`: Count of credential harvesting keywords ("password", "pin", "ssn").
  - `mismatched_href_count`: Count of HTML anchors where visible link text differs from destination domain.
  - `shortener_in_text`: Presence of known URL shorteners.

---

## 3. Leakage Prevention: Domain-Grouped Splits

Random train/test splits cause severe data leakage because multiple URLs sharing the same registered domain (eTLD+1) end up on both sides of the split.

**Splitting Protocol:**
- Extract registered domains using `tldextract`.
- Split using `sklearn.model_selection.GroupShuffleSplit` grouped on `registered_domain`.
- **Split Proportions**:
  - **Train Set (70%)**: Used for model fitting and internal 5-fold cross-validation.
  - **Validation Set (10%)**: Used **exclusively** for probability calibration and F2 threshold selection.
  - **Test Set (20%)**: Held-out, touched **only once** for final reporting.

### 3.1 Out-of-Distribution Fresh Evaluation Set
A secondary held-out set of **500 fresh phishing URLs** and **500 fresh benign URLs** collected at least 14 days after the primary dataset cutoff. Evaluates real-world performance against zero-day campaigns.

---

## 4. Modeling Strategy

### 4.1 Experiment Matrix

| Architecture | Class Imbalance Strategy | Calibration Method | Explainer Type |
|---|---|---|---|
| **Logistic Regression (Baseline)** | `class_weight='balanced'` | Platt Scaling (Sigmoid) | `shap.LinearExplainer` |
| **Random Forest** | `class_weight='balanced'` | Isotonic Regression | `shap.TreeExplainer` |
| **XGBoost** | `scale_pos_weight` | Isotonic Regression | `shap.TreeExplainer` |
| **LightGBM (Primary Candidate)** | `is_unbalance=True` | Isotonic Regression | `shap.TreeExplainer` |

### 4.2 Hyperparameter Optimization
Hyperparameter search is conducted using `Optuna` (50 trials per model) via **5-fold GroupKFold Cross-Validation strictly inside the 70% Train set**. The validation set is never touched during hyperparameter tuning.

### 4.3 Calibration & Decision Threshold
- **Probability Calibration**: Uses `CalibratedClassifierCV` fitted on the 10% validation split. (Compatible with modern scikit-learn $\ge$ 1.2 frozen estimator standards).
- **Threshold Optimization**: Decision threshold $\tau$ is chosen on the validation split to maximize the **$F_2$ score** ($\beta = 2$), prioritizing recall over precision because false negatives (missed attacks) carry catastrophic security consequences.

---

## 5. Rigorous Evaluation Protocol

### 5.1 Metrics & Statistical Bounds
1. **$F_2$ Score & F1 Score**: Calculated at the optimal threshold $\tau$.
2. **Precision, Recall, ROC-AUC, PR-AUC**.
3. **Bootstrap 95% Confidence Intervals**: Derived via 1,000 bootstrap resamples on the test split to prove statistical significance.
4. **False Positive Rate on Top Benign Domains**: Tested against the Tranco Top-500 legitimate domains (Target: $\text{FPR} < 0.2\%$).
5. **Expected Calibration Error (ECE)** & Reliability Curve.
6. **Inference Latency**: Median and 95th percentile latency benchmarked over 1,000 inputs.

### 5.2 Explainability Framework (SHAP)
- **Local Explanations**: TreeExplainer outputs the top-10 directional feature contributions for each inference.
- **Mathematical Transparency**: Documentation and UI explicitly state that **SHAP explains the raw model log-odds output**, whereas the verdict dial displays the **calibrated probability**.

---

## 6. Makefile Pipeline Targets

| Target | Pipeline Action |
|---|---|
| `make data` | Downloads raw datasets and generates verifiable `manifest.json` |
| `make features` | Extracts lexical/text features and creates domain-grouped splits |
| `make tune` | Runs Optuna 5-fold cross-validation on train split |
| `make train` | Fits candidate models and calibrates on validation split |
| `make evaluate` | Generates metrics with 95% CIs and curves in `models/eval/` |
| `make fresh-eval` | Benchmarks against the post-cutoff fresh feed |
| `make test` | Executes unit tests and data validation checks |
| `make all` | Full reproducible pipeline execution from scratch |