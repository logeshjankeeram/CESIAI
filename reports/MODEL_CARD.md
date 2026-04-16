# Model Card — Diabetes Risk MLP (Sprint 3)

**Intended use**: clinical decision support — *screening* for diabetes risk. Not a diagnostic.

**Model**: Keras Sequential MLP, 128 → 64 → 32 → 1 (ReLU + BatchNorm + Dropout 0.3 + L2 1e-4).
**Training**: Adam lr=5e-4, batch 256, early stopping patience 8 on val AUC.
**Imbalance strategy**: class_weighted.

## Data
- Source: BRFSS 2015 (CDC), via Kaggle.
- Rows: 229,474 after cleaning, 70/15/15 split.
- Positive rate: 15.3%.
- Data hashes: see `logs/experiment_log.json` → `data_ids`.

## Metrics (held-out test set)
- AUC-ROC: **0.8175**
- F1 at clinical threshold (0.55): **0.4619**
- Recall: 0.750
- Precision: 0.334
- Missed diabetics (FN): 1316
- False alarms (FP): 7886

## Threshold guidance
- Default 0.5: high precision, low recall — NOT suitable for screening.
- Clinical 0.55: calibrated to catch ≥75% of positives. Confirm with Dr. Naye Wells before deployment.

## Known limits
- Self-reported BRFSS data → measurement noise on BMI, physical activity.
- US 2015 population → transfer to other years/countries not validated.
- No subgroup fairness audit yet beyond the sex split below.
- Not a medical device. CE marking / EU AI Act Annex III obligations apply before any clinical rollout.

## Environmental cost (this training run)
- Training time (winner): 26.9 s on macOS-15.2-arm64-arm-64bit
- See section 5 for the detailed CO2-proxy estimate.
