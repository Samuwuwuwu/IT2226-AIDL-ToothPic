# Initial architecture

```text
Browser -> Vite :5173 -> /api/v1 proxy -> FastAPI :8000
                                         -> future model inference
                                         -> future agent / clinic and subsidy tools

Colab or local -> shared ml/src/aidl_ml training -> versioned checkpoint
                                            -> later loaded by the API
```

**Implemented:** `GET /api/v1/health` and a web API connectivity indicator.

**Not implemented:** camera capture, trained model inference, LLM/agent, fee engine, clinic locator, persistence or deployment. No fabricated predictions.

Keep frontend requests in `apps/web/src/services/api.ts`, application logic on the API side, training code in `ml/src/aidl_ml` and large data/artifacts out of Git.
