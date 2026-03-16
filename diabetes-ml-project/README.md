## Diabetes ML Project – BRFSS 2015

This project builds end-to-end machine learning and deep learning models to **predict diabetes** using the **Diabetes Health Indicators (BRFSS 2015)** dataset.

The goal is to follow solid **data science engineering practices**: clean data preparation, clear experiment tracking, modular code, and reproducible results.

### Dataset

- **Name**: Diabetes Health Indicators (BRFSS 2015)
- **Source**: Kaggle (`alexteboul/diabetes-health-indicators-dataset`)
- **Main file**: `diabetes_binary_health_indicators_BRFSS2015.csv`
- **Target variable**: `Diabetes_binary` (1 = diabetes / pre-diabetes, 0 = no diabetes)

Place the raw CSV file in:

- `data/raw/diabetes_binary_health_indicators_BRFSS2015.csv`

### Project Structure

```text
diabetes-ml-project/
│
├── data/
│   ├── raw/          # Original, immutable data dumps
│   ├── interim/      # Intermediate data (e.g., partially cleaned)
│   └── processed/    # Final, cleaned data ready for modeling
│
├── notebooks/
│   ├── 01_data_preparation.ipynb   # Deliverable 1 – EDA & preprocessing
│   ├── 02_baseline_model.ipynb     # Deliverable 2 – baseline models
│   ├── 03_model_improvement.ipynb  # Hyperparameter tuning, advanced models
│   └── 04_explainability.ipynb     # SHAP, feature importance, explanations
│
├── src/
│   ├── data_preprocessing.py       # Loading, cleaning, splitting, scaling
│   ├── train_model.py              # Training models and saving them
│   ├── evaluate_model.py           # Metrics and evaluation utilities
│   ├── model_architecture.py       # Neural network architectures
│   └── utils.py                    # Shared helper functions
│
├── models/                         # Saved trained models / weights
│
├── figures/
│   ├── eda_plots/                  # Plots from exploratory analysis
│   └── model_results/              # Plots of model performance
│
├── reports/
│   ├── deliverable_1_data_preparation.md
│   ├── deliverable_2_model_training.md
│   └── final_report.md
│
├── requirements.txt
├── README.md
└── .gitignore
```

### Setup

From the project root:

```bash
cd diabetes-ml-project
python3 -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Running the Notebooks

1. Ensure the raw dataset is available at:

   - `data/raw/diabetes_binary_health_indicators_BRFSS2015.csv`

2. Start Jupyter:

   ```bash
   cd diabetes-ml-project
   jupyter notebook
   ```

3. Run notebooks in order:

   1. `notebooks/01_data_preparation.ipynb`
   2. `notebooks/02_baseline_model.ipynb`
   3. `notebooks/03_model_improvement.ipynb`
   4. `notebooks/04_explainability.ipynb`

Each notebook should use **relative paths** such as:

- `../data/raw/`
- `../data/processed/`

to load and save data.

### Coding Guidelines

- Keep data preparation logic in `src/data_preprocessing.py` and call it from notebooks.
- Avoid data leakage by:
  - Splitting into train/validation/test before fitting scalers or models.
  - Fitting preprocessing (e.g., `StandardScaler`) on **train only**, then applying to validation/test.
- Store trained models in `models/` and results figures in `figures/`.
- Use clear function docstrings and type hints where possible.

