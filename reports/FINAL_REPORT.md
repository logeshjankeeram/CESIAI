### Architecture (final)

3-layer MLP: Input(21) → Dense(128, BN, ReLU, Drop 0.3, L2 1e-4) → Dense(64, BN, ReLU, Drop 0.3, L2 1e-4) → Dense(32, ReLU) → Dense(1, Sigmoid). Adam lr=5e-4, batch 256, early stopping patience 8 on val AUC.

### Results vs. Sprint 2

| Model | Test AUC | Test F1 (clinical thresh.) | Notes |
|---|---|---|---|
| LR baseline (Sprint 2) | 0.8070 | 0.24 | linear, no SMOTE |
| MLP baseline (Sprint 2) | 0.8156 | 0.27 | 64-32, no regularisation |
| MLP + Dropout (Sprint 2) | 0.8162 | 0.12 | over-regularised at 0.5 |
| **Advanced MLP (Sprint 3, winner)** | **0.8175** | **0.4619** | 128-64-32, BN+Drop+L2, class_weighted |

AUC moved from ~0.816 (Sprint 2) to 0.8175. The bigger shift is on recall at the clinical threshold — class_weighted pulls missed diabetics down versus the Sprint 2 MLP at the same threshold.

### Framework

TensorFlow/Keras. Kept from Sprint 2. Reasons in §2.

### Imbalance

Class-weighting and SMOTE both tried; winner on val AUC was `class_weighted`. Threshold re-tuned on val (clinical = 0.55, recall ≥ 0.75).

### MLOps

- Data versioned via sha1 hashes stored per run.
- Env snapshot (Git SHA, Python, TF, numpy, pandas) logged per run.
- `experiment_log.json` extended from Sprint 2, still greppable, no MLflow overhead.
- sklearn / imblearn `Pipeline` for the LR baseline; Keras model saved as `.keras` + meta JSON.
- Automation skeleton: `pipeline.py` at the repo root mirrors the notebook.
- Model card written for the CECN (`reports/MODEL_CARD.md`).

### Explainable AI

SHAP DeepExplainer on a 2000-patient test sample. Top global drivers: see the global bar plot in §5a. Local explanations available per patient for doctor challenge.

### Sustainable development

Training cost logged per run via a time × power × grid-intensity proxy (§5d). Winner run: ~0.00037 kWh, ~0.022 g CO₂eq. Model kept intentionally shallow (frugal-AI principle from AFNOR SPEC 2314). CodeCarbon / GenAI-Impact would refine this — out of scope for the sprint but flagged.

### Ethics

Quick Sex-subgroup audit in §5c. Full audit on Age / Income / Education is the next priority before any clinical pilot. EU AI Act: Annex III high-risk — needs CE marking and documented human-oversight protocol. GDPR: no PII in the dataset, no re-identification attempted.

### What we'd do next

- Full subgroup fairness audit + mitigation (re-weighting or FairBalance per the Loop 5 resources).
- Move data versioning from sha1-in-JSON to DVC once the dataset starts evolving.
- Replace the CO₂ proxy with CodeCarbon.
- Calibration (Platt / isotonic) so the probability itself is clinically meaningful, not just the threshold.
- External validation on a non-US cohort before any pilot.
