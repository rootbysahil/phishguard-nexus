# ADR-002: LLM Provider Interface Pattern

**Status:** Accepted  
**Phase:** Phase 0 — Architecture  
**Deciders:** Engineering team

---

## Context

The product vision requires IBM watsonx.ai Granite to generate plain-language threat
explanations in three languages. However:

1. Not every reviewer or demo environment will have IBM watsonx.ai credentials.
2. CI pipelines must not call external paid APIs.
3. The app must be fully demonstrable offline (e.g., in a conference or classroom setting).
4. A future version may swap the LLM provider without touching the rest of the codebase.

## Decision

Define an abstract `LLMProvider` base class with a single method:

```python
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, context: dict, lang: str) -> str:
        ...
```

Ship two concrete implementations:

| Implementation | File | When Used |
|---|---|---|
| `WatsonxProvider` | `llm/watsonx_provider.py` | `WATSONX_API_KEY` is set in `.env` |
| `TemplateFallbackProvider` | `llm/template_provider.py` | API key absent or service unreachable |

The app factory in `main.py` selects the active provider at startup and injects it via
FastAPI dependency injection. No route handler knows which provider is active.

## Rationale

- **Separation of concerns:** the ML pipeline, explanation logic, and LLM transport are
  independent layers.
- **Testability:** unit tests use the `TemplateFallbackProvider` without mocking HTTP calls.
- **Interview-readiness:** the pattern demonstrates knowledge of the Strategy design pattern
  and dependency inversion — directly relevant to IBM internship technical reviews.
- **Resilience:** if watsonx.ai is temporarily unreachable, the fallback activates
  transparently; the UI shows an "Offline Mode" badge.

## Template Fallback Design

The `TemplateFallbackProvider` produces deterministic, human-readable explanations using
a decision-tree of the top SHAP features and verdict. It is not an LLM — it is a
structured template fill. The UI clearly labels it as "Offline Mode — AI Unavailable"
so the user is never misled.

The template outputs are pre-translated strings for EN, HI (Hindi), and PA (Punjabi),
keyed by verdict and top-feature combination.

## Consequences

- `WATSONX_API_KEY`, `WATSONX_PROJECT_ID`, and `WATSONX_URL` are in `.env.example` with
  placeholder values and are never required to run the app.
- The `TemplateFallbackProvider` is always tested in CI.
- `WatsonxProvider` is integration-tested only when credentials are available
  (guarded by a `pytest.mark.requires_watsonx` skip marker).

## Security Note

Raw user input is **never** forwarded to the LLM. The `context` dict passed to
`generate()` contains only verified, structured findings (verdict, top-5 SHAP features,
red flag strings). This eliminates prompt-injection risk from the scanned content.

## Rejected Alternatives

**Hardcoded watsonx.ai calls in the route handler:** Rejected because it would make the
app non-functional without credentials and untestable in CI.

**OpenAI / Anthropic as alternative LLM:** Rejected per working rule 6 (ask before major
decisions, prefer free and open-source). IBM watsonx.ai is the required provider for this
IBM internship project.
