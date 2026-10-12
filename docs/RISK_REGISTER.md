# PHISHGUARD//NEXUS — Risk Register

> Phase 0 planning document.
> Project risk matrix, severity classifications, and technical mitigations.

---

## Risk Rating Key

| Probability | Description |
|---|---|
| High | Likely to occur without active mitigation |
| Medium | May occur; manageable with awareness |
| Low | Unlikely; noted for completeness |

| Impact | Description |
|---|---|
| Critical | Breaks the core demo or introduces a security vulnerability |
| High | Degrades a major feature significantly |
| Medium | Requires workaround; demo still runs |
| Low | Cosmetic or minor inconvenience |

---

## Risk Table

| ID | Risk | Prob | Impact | Mitigation | Owner Phase |
|---|---|---|---|---|---|
| R-01 | PhishTank changes its API schema or rate-limits aggressively | Medium | High | Download is script-based and cached locally. UCI + Kaggle datasets serve as primary fallback. Document fallback procedure in `docs/DATASETS.md`. | Phase 2 |
| R-02 | IBM watsonx.ai API quota exhausted during live demo | Medium | Medium | Template-based `LLMProvider` fallback is always active and fully featured. Quota remaining is surfaced in the UI status bar. | Phase 4 |
| R-03 | 3D globe causes performance drop on low-end / integrated GPU | Medium | Medium | Globe is lazy-loaded and behind a dynamic import. "Reduced Effects" mode in Settings disables the WebGL scene entirely and replaces it with a static 2D SVG map. | Phase 6 |
| R-04 | ML model overfits due to accidental data leakage from random URL split | High (without mitigation) | Critical | Enforced group split by registered domain (ADR-003) eliminates this. Documented in `ML_PLAN.md` and `MODEL_CARD.md`. | Phase 2–3 |
| R-05 | SHAP explanation latency is unacceptably high in production | Low | Medium | `TreeExplainer` is fast (< 20 ms for tree models). SHAP is capped at top-50 features per prediction. Per-prediction SHAP is called asynchronously and streamed as its own pipeline stage. | Phase 4 |
| R-06 | Model artifacts exceed GitHub's 100 MB file limit | Medium | Medium | Model files are gitignored. Git LFS or DVC is used to track them. `make train` reproduces them from scratch. README documents this clearly. | Phase 3 |
| R-07 | Raw email / SMS content accidentally logged or persisted | Low | Critical | Architecture rule: raw text is handled only in memory during the scan request. The DB schema stores only SHA-256 hash + extracted features. Logging config filters the `content` field. | Phase 4 |
| R-08 | Prompt injection via scanned content reaching the LLM | Low | High | The LLM receives only a structured JSON object of verified findings. Raw user input is never forwarded to the LLM prompt. LLM outputs are sanitized. (ADR-002) | Phase 4 |
| R-09 | SSRF via scanned URL if live fetching is ever enabled | Medium | Critical | Live URL fetching is off by default. If host-feature checks are enabled, only the registered domain is queried. Private / loopback / link-local IPs are blocked at the resolver. Hard timeouts and size limits are enforced. (ADR-005) | Phase 4 |
| R-10 | Browser extension MV3 API changes or Chrome Web Store policy update | Low | Low | Extension is a Phase 7 stretch goal and explicitly optional. It is kept in a separate directory and has no impact on the core app. | Phase 7 |
| R-11 | Fabricated metrics in README or UI (violates working rule 3) | High (without discipline) | Critical | All numeric values in README and UI are placeholders (`—` or `[PENDING]`) until populated by real `make evaluate` output. Model Lab page shows a banner if artifact files are missing. | All phases |
| R-12 | Calibrated probability is poorly calibrated, making the confidence score misleading | Medium | High | `CalibratedClassifierCV` with isotonic regression is applied. Calibration is validated with a reliability diagram and ECE metric. Both are reported in MODEL_CARD.md. | Phase 3 |
| R-13 | Fresh-URL evaluation reveals major generalization gap | Medium | Medium | This is expected and acceptable if honestly reported. The fresh-URL section in MODEL_CARD.md explicitly discusses failure modes. The UI shows no fake "99% accuracy" claims. | Phase 3 |
| R-14 | Docker compose fails on Windows due to path / line-ending issues | Medium | Medium | All shell scripts use POSIX line endings (enforced by `.gitattributes`). Docker volumes use forward slashes. CI runs on Ubuntu to verify. | Phase 1 |
| R-15 | Playwright end-to-end test is flaky due to animation timing | Low | Low | E2E test uses `waitForSelector` and `waitForResponse`, never fixed `sleep()` calls. Animations are disabled in the Playwright config via `prefers-reduced-motion`. | Phase 7 |
