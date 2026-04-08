from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether
)

OUTPUT = "Deep_Learning_Project_Report.pdf"
W, H = A4

# ── Styles ─────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def style(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=base[parent], **kw)

cover_title  = style("CoverTitle",  "Title",   fontSize=28, textColor=colors.HexColor("#1a1a2e"), spaceAfter=8,  alignment=TA_CENTER, leading=34)
cover_sub    = style("CoverSub",    "Normal",  fontSize=14, textColor=colors.HexColor("#16213e"), spaceAfter=6,  alignment=TA_CENTER)
cover_meta   = style("CoverMeta",   "Normal",  fontSize=11, textColor=colors.HexColor("#555"),    spaceAfter=4,  alignment=TA_CENTER)

h1           = style("H1",          "Heading1", fontSize=16, textColor=colors.HexColor("#1a1a2e"), spaceBefore=18, spaceAfter=6,  borderPad=0)
h2           = style("H2",          "Heading2", fontSize=13, textColor=colors.HexColor("#16213e"), spaceBefore=12, spaceAfter=4)
h3           = style("H3",          "Heading3", fontSize=11, textColor=colors.HexColor("#333"),    spaceBefore=8,  spaceAfter=3,  fontName="Helvetica-Bold")
body         = style("Body",        "Normal",   fontSize=10, leading=16, spaceAfter=6,  alignment=TA_JUSTIFY)
body_left    = style("BodyL",       "Normal",   fontSize=10, leading=16, spaceAfter=6)
bullet_s     = style("Bullet",      "Normal",   fontSize=10, leading=15, spaceAfter=3,  leftIndent=16, bulletIndent=6)
code_s       = style("Code",        "Code",     fontSize=8.5,leading=13, spaceAfter=4,  backColor=colors.HexColor("#f4f4f4"), fontName="Courier", leftIndent=12)
caption      = style("Caption",     "Normal",   fontSize=9,  textColor=colors.HexColor("#666"), spaceAfter=8, alignment=TA_CENTER)
note_s       = style("Note",        "Normal",   fontSize=9,  textColor=colors.HexColor("#444"), leading=14, spaceAfter=4, leftIndent=12, borderPad=4)
label_s      = style("Label",       "Normal",   fontSize=9,  textColor=colors.white, fontName="Helvetica-Bold", alignment=TA_CENTER)

def hr(): return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc"), spaceAfter=6, spaceBefore=6)
def sp(n=6): return Spacer(1, n)
def p(txt, st=None): return Paragraph(txt, st or body)
def b(txt): return Paragraph(f"• {txt}", bullet_s)
def h(txt, level=1): return Paragraph(txt, [h1, h2, h3][level-1])
def code(txt): return Paragraph(txt.replace(" ", "&nbsp;").replace("\n", "<br/>"), code_s)

def section_label(txt, color="#1a1a2e"):
    data = [[Paragraph(txt, label_s)]]
    t = Table(data, colWidths=[16*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor(color)),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return t

def info_box(txt, bg="#eef2ff"):
    data = [[Paragraph(txt, note_s)]]
    t = Table(data, colWidths=[16*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor(bg)),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("BOX",           (0,0), (-1,-1), 0.5, colors.HexColor("#b0b8d0")),
    ]))
    return t

def two_col_table(rows, col_widths=None, header=None):
    cw = col_widths or [5*cm, 11*cm]
    data = []
    if header:
        data.append(header)
    data.extend(rows)
    t = Table(data, colWidths=cw)
    ts = [
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("LEADING",       (0,0), (-1,-1), 13),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("ROWBACKGROUNDS",(0,0), (-1,-1), [colors.HexColor("#f9f9f9"), colors.white]),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#dddddd")),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]
    if header:
        ts += [
            ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#1a1a2e")),
            ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
            ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ]
    t.setStyle(TableStyle(ts))
    return t

# ── Page template with footer ───────────────────────────────────────────────
def make_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#888"))
    canvas.drawString(2*cm, 1.2*cm, "CESI Ecole d'Ingenieurs — Deep Learning Project — Diabetes Prediction")
    canvas.drawRightString(W - 2*cm, 1.2*cm, f"Page {doc.page}")
    canvas.restoreState()

def make_cover_footer(canvas, doc):
    pass  # no footer on cover

# ── Build content ───────────────────────────────────────────────────────────
story = []

# ═══════════════════════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════════════════════
story.append(sp(60))

# colour block title
data = [[Paragraph("DEEP LEARNING PROJECT", style("CT2","Normal",fontSize=22,textColor=colors.white,fontName="Helvetica-Bold",alignment=TA_CENTER))]]
t = Table(data, colWidths=[16*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#1a1a2e")),
    ("TOPPADDING",    (0,0), (-1,-1), 18),
    ("BOTTOMPADDING", (0,0), (-1,-1), 18),
]))
story.append(t)
story.append(sp(4))
data = [[Paragraph("Diabetes Risk Prediction using Neural Networks", style("CT3","Normal",fontSize=13,textColor=colors.white,alignment=TA_CENTER))]]
t = Table(data, colWidths=[16*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#16213e")),
    ("TOPPADDING",    (0,0), (-1,-1), 10),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
]))
story.append(t)
story.append(sp(40))

for line, sz, clr in [
    ("CESI Ecole d'Ingenieurs", 12, "#333"),
    ("ETU EN — Projet Deep Learning", 11, "#555"),
    ("Sprint 1 + Sprint 2 — Deliverables 1 and 2", 11, "#555"),
    ("April 2026", 11, "#777"),
]:
    story.append(Paragraph(line, style(f"cl{sz}","Normal",fontSize=sz,textColor=colors.HexColor(clr),alignment=TA_CENTER,spaceAfter=5)))

story.append(sp(50))
story.append(hr())
story.append(Paragraph("Dataset: Diabetes Health Indicators — BRFSS 2015 (Kaggle)", caption))
story.append(Paragraph("Primary metric: AUC-ROC", caption))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# INTRODUCTION
# ═══════════════════════════════════════════════════════════
story.append(h("Introduction"))
story.append(hr())
story.append(p("The Data Science team at Saint-Charles University Hospital is developing a clinical decision support tool to predict the risk of diabetes. The goal is to help physicians identify at-risk patients early so that treatment and lifestyle interventions can be applied before the disease progresses."))
story.append(p("This report documents the work done across two sprints. Sprint 1 covers data cleaning and preparation (Deliverable 1). Sprint 2 covers building and evaluating an initial neural network (Deliverable 2). A third sprint covering advanced optimisation and explainability is planned but not included here."))
story.append(sp(4))
story.append(h("Dataset", 2))
story.append(p("The Behavioral Risk Factor Surveillance System (BRFSS) 2015 dataset is a large telephone health survey collected by the CDC. The version used here contains 253,680 responses and 22 variables. The target variable is Diabetes_binary (1 = diabetes or pre-diabetes, 0 = no diabetes). The dataset has a significant class imbalance: roughly 85% of responses are class 0."))
story.append(sp(4))
story.append(two_col_table([
    ["253,680", "Total rows"],
    ["21",      "Input features after removing target"],
    ["~15%",    "Positive class rate (diabetic)"],
    ["BRFSS 2015", "Source survey"],
    ["AUC-ROC", "Primary evaluation metric"],
], header=["Fact", "Detail"]))
story.append(sp(8))
story.append(h("Project structure", 2))
story.append(b("notebook 01_data_preparation.ipynb — Deliverable 1: full preprocessing pipeline"))
story.append(b("notebook 02_neural_network.ipynb — Deliverable 2: model training and evaluation"))
story.append(b("data/processed/ — cleaned and split CSV files produced by notebook 01"))
story.append(b("models/ — saved trained model"))
story.append(b("logs/ — training CSVs, plots, experiment log JSON"))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# HOW TO RUN
# ═══════════════════════════════════════════════════════════
story.append(h("How to Run the Project"))
story.append(hr())
story.append(info_box("This section assumes you have never used a Mac terminal or Jupyter before. Every step is shown explicitly. Follow them in order.", "#fff8e1"))
story.append(sp(8))

story.append(h("Step 1 — Open the Terminal", 2))
story.append(p("The Terminal is the text interface for your Mac. You type commands and the Mac executes them."))
story.append(b("Press Command + Space to open Spotlight search."))
story.append(b('Type "Terminal" and press Enter.'))
story.append(b("A black or white window opens with a prompt ending in %. That is the Terminal."))
story.append(sp(6))

story.append(h("Step 2 — Navigate to the project folder", 2))
story.append(p("You need to tell the Terminal where the project lives. Type the following command exactly and press Enter:"))
story.append(code("cd /Users/logeshjankeeram/Desktop/CESI/AI"))
story.append(p("cd means change directory. After pressing Enter you will see no output — that is normal. The prompt now points to the AI folder."))
story.append(sp(6))

story.append(h("Step 3 — Confirm the files are there", 2))
story.append(p("Type the following and press Enter to list the files:"))
story.append(code("ls"))
story.append(p("You should see at minimum: 01_data_preparation.ipynb, 02_neural_network.ipynb, and a data folder. If you see those the setup is correct."))
story.append(sp(6))

story.append(h("Step 4 — Start JupyterLab", 2))
story.append(p("JupyterLab is the browser-based interface for running the notebooks. Jupyter was installed in a non-standard location so you must use the full path:"))
story.append(code("/Users/logeshjankeeram/Library/Python/3.9/bin/jupyter lab"))
story.append(p("Press Enter. You will see some lines of text appear. After a few seconds your default browser will open automatically with a JupyterLab tab. Do not close the Terminal while working — it must stay open."))
story.append(info_box("If the browser does not open automatically, look in the Terminal output for a line starting with http://localhost:8888/... and copy-paste that URL into your browser.", "#f0fff0"))
story.append(sp(6))

story.append(h("Step 5 — Run Deliverable 1 first", 2))
story.append(p("In the JupyterLab file panel on the left, double-click 01_data_preparation.ipynb. The notebook opens in a new tab."))
story.append(b("In the top menu click Run."))
story.append(b("Click Run All Cells."))
story.append(b("Wait for all cells to finish. A cell is running when it shows [*] on the left. It is done when it shows a number like [1], [2], etc."))
story.append(b("The last cell should print a message confirming files were saved to data/processed/."))
story.append(info_box("Notebook 01 must complete before notebook 02 can run. Notebook 02 reads the CSV files that notebook 01 creates.", "#fff8e1"))
story.append(sp(6))

story.append(h("Step 6 — Run Deliverable 2", 2))
story.append(p("Double-click 02_neural_network.ipynb in the file panel. Then:"))
story.append(b("Click Run then Run All Cells."))
story.append(b("This notebook trains three neural network models and one logistic regression. It will take 2 to 5 minutes depending on your machine."))
story.append(b("Progress is printed after each training epoch. Early stopping will print a message when it stops training."))
story.append(b("When finished the logs/ folder will contain plots, CSVs and an experiment_log.json file. The models/ folder will contain mlp_baseline.keras."))
story.append(sp(6))

story.append(h("Stopping JupyterLab", 2))
story.append(p("When you are done, go back to the Terminal and press Control + C. Type y and press Enter to confirm shutdown."))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# PART 1 — DELIVERABLE 1
# ═══════════════════════════════════════════════════════════
data = [[Paragraph("PART 1 — DELIVERABLE 1: DATA PREPARATION", style("PL","Normal",fontSize=14,textColor=colors.white,fontName="Helvetica-Bold",alignment=TA_CENTER))]]
t = Table(data, colWidths=[16*cm])
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#1a1a2e")),("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),14)]))
story.append(t)
story.append(sp(12))

story.append(p("Notebook: 01_data_preparation.ipynb. This notebook takes the raw CSV and produces clean, split, normalised datasets ready for modelling. Nothing from the validation or test sets is ever used to inform preprocessing decisions — this is the fundamental rule against data leakage."))
story.append(sp(8))

# Step 1
story.append(h("Step 1 — Load and Inspect", 2))
story.append(p("The raw CSV is loaded with pandas. The first thing to check is shape (how many rows and columns), data types, summary statistics, and the target distribution. This gives an overall picture of what we are working with before touching anything."))
story.append(b("Shape: 253,680 rows, 22 columns."))
story.append(b("All values are already numeric (integers or floats). No string columns to encode."))
story.append(b("Target: Diabetes_binary. Value 0 means no diabetes. Value 1 means diabetes or pre-diabetes."))
story.append(b("Class distribution: roughly 14-15% of rows are class 1. The dataset is imbalanced."))
story.append(sp(4))
story.append(info_box("The class imbalance (85/15 split) means accuracy is not a good standalone metric. A model that always predicts 0 would get 85% accuracy while being completely useless. AUC-ROC is more informative here.", "#fff3cd"))

story.append(sp(8))
story.append(h("Step 2 — Separate X and y", 2))
story.append(p("The target column (Diabetes_binary) is separated from the 21 feature columns before any splitting or preprocessing. This is done early to make sure there is no accidental use of y values during feature engineering."))
story.append(b("y = the target column (what we want to predict)."))
story.append(b("X = the remaining 21 columns (the inputs to the model)."))

story.append(sp(8))
story.append(h("Step 3 — Train / Validation / Test Split", 2))
story.append(p("The data is divided into three non-overlapping sets:"))
story.append(two_col_table([
    ["Train (70%)",      "160,631 rows. The model learns from this set only."],
    ["Validation (15%)", "34,421 rows. Used after each training epoch to monitor generalisation. Never trained on."],
    ["Test (15%)",       "34,422 rows. Touched only at the very end for the final honest score."],
], header=["Split", "Purpose"]))
story.append(sp(6))
story.append(p("Stratified splitting is used. This means the class ratio (85/15) is preserved in each of the three sets. Without stratification, one split could end up with a different ratio purely by chance, which would make comparisons misleading."))
story.append(b("Random state is fixed at 42 so the split is reproducible."))

story.append(sp(8))
story.append(h("Step 4 — Variable Types", 2))
story.append(p("The 21 features are grouped into three types. This matters because different preprocessing applies to different types."))
story.append(two_col_table([
    ["Binary (14 vars)",   "HighBP, HighChol, Smoker, Stroke, Sex, etc. Already 0/1. No scaling needed."],
    ["Ordinal (4 vars)",   "GenHlth, Age, Education, Income. Integer scales with ordered categories. Treated as numeric."],
    ["Continuous (3 vars)","BMI, MentHlth, PhysHlth. Real-valued. These get scaled."],
], header=["Type", "Variables and treatment"]))

story.append(sp(8))
story.append(h("Step 5 — Duplicates and Missing Values", 2))
story.append(p("Two checks are run on the full dataset before splitting. First, duplicate rows are identified and removed. Second, missing values (NaN) are counted per column."))
story.append(b("Result: no missing values found. All 22 columns are complete."))
story.append(b("Duplicate rows exist and are removed before re-splitting."))
story.append(p("If imputation had been needed (e.g. filling missing BMI values with the median), it would have been fit only on the training set and then applied to val and test. Computing the median on the full dataset before splitting would be data leakage because it would include information from the test set."))

story.append(sp(8))
story.append(h("Step 6 — Quantitative EDA", 2))
story.append(p("Basic descriptive statistics (mean, median, std, quartiles) are computed on the training set. Then Pearson correlation coefficients between each feature and the target are computed, also on training data only."))
story.append(b("Strongest positive correlates with diabetes: HighBP, BMI, GenHlth (poor health), DiffWalk, Age."))
story.append(b("Strongest negative correlates: Income, Education, PhysActivity."))
story.append(b("No extreme multicollinearity found between features."))

story.append(sp(8))
story.append(h("Step 7 — Qualitative EDA", 2))
story.append(p("Six visualisations are produced, all using training data only:"))
story.append(b("Class distribution bar chart: confirms the 85/15 imbalance."))
story.append(b("BMI histogram: right-skewed distribution with a tail above 50. StandardScaler handles this."))
story.append(b("Age bar chart: ordinal categories 1-13. Older groups are more represented."))
story.append(b("BMI boxplot by class: diabetic group has a noticeably higher BMI median."))
story.append(b("Bar charts for HighBP, HighChol, PhysActivity, DiffWalk: all show a clear difference in diabetes rate between groups."))
story.append(b("Correlation heatmap: visual confirmation of the top correlates identified in Step 6."))

story.append(sp(8))
story.append(h("Step 8 — Normalisation", 2))
story.append(p("StandardScaler is applied to the three continuous features (BMI, MentHlth, PhysHlth). It transforms each feature to have zero mean and unit standard deviation."))
story.append(code("scaled_value = (original_value - mean_train) / std_train"))
story.append(p("The scaler is fit on the training set only. The same mean and std values are then used to transform the validation and test sets. This is critical: if the scaler were fit on the full dataset, the mean and std would contain information from the test set, which would be data leakage."))
story.append(b("Binary and ordinal features are left untouched."))
story.append(b("The fitted scaler is saved to data/processed/standard_scaler.joblib so it can be reused at inference time."))

story.append(sp(8))
story.append(h("Step 9 — Save", 2))
story.append(p("Six CSV files and the scaler are written to data/processed/:"))
story.append(b("X_train.csv, X_val.csv, X_test.csv — scaled feature matrices."))
story.append(b("y_train.csv, y_val.csv, y_test.csv — corresponding target vectors."))
story.append(b("standard_scaler.joblib — the fitted StandardScaler object."))
story.append(p("Saving here decouples preprocessing from modelling. Notebook 02 can be re-run without re-running notebook 01."))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# PART 2 — DELIVERABLE 2
# ═══════════════════════════════════════════════════════════
data = [[Paragraph("PART 2 — DELIVERABLE 2: NEURAL NETWORK", style("PL2","Normal",fontSize=14,textColor=colors.white,fontName="Helvetica-Bold",alignment=TA_CENTER))]]
t = Table(data, colWidths=[16*cm])
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#16213e")),("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),14)]))
story.append(t)
story.append(sp(12))

story.append(p("Notebook: 02_neural_network.ipynb. This notebook loads the processed data from Deliverable 1, trains a neural network, evaluates it, and logs all results. It also trains two regularised variants and a logistic regression baseline for comparison."))
story.append(sp(8))

story.append(h("Section 1 — Architecture Choice", 2))
story.append(p("The starting point for this sprint is the Loop 2 prototype: 1 hidden layer, 5 neurons, batch size 32, trained on 240 rows. That prototype reached ~65% accuracy and was unstable. Deliverable 2 trains on the full 160k row dataset with a deeper, wider network."))
story.append(sp(4))
story.append(p("A Multi-Layer Perceptron (MLP) was chosen because the data is tabular. Convolutional networks (CNN) are for images. Recurrent networks (RNN) are for sequences. Neither applies here. MLP with two hidden layers is the standard architecture for structured tabular data."))
story.append(sp(6))

story.append(info_box(
    "Architecture: Input(21) -> Dense(64, ReLU) -> Dense(32, ReLU) -> Dense(1, Sigmoid)\n\n"
    "3,521 trainable parameters total. The funnel shape (64 -> 32) forces the network to compress the information progressively.",
    "#eef2ff"
))
story.append(sp(6))

story.append(two_col_table([
    ["ReLU (hidden layers)",       "Standard activation. Avoids vanishing gradient. Fast to compute. f(x) = max(0, x)."],
    ["Sigmoid (output)",           "Maps output to probability in [0,1]. Required for binary classification."],
    ["Binary cross-entropy (loss)","Standard loss for binary classification. Penalises confident wrong predictions heavily."],
    ["Adam, lr=0.001",             "Adaptive optimiser. Adjusts learning rate per parameter. Robust default."],
    ["Batch size 256",             "Processes 256 rows per weight update. Stable gradients on 160k rows."],
    ["Early stopping, patience=5", "Stops training if val AUC does not improve for 5 consecutive epochs. Saves best weights."],
], header=["Choice", "Reason"]))

story.append(sp(8))
story.append(h("Section 2 — Logistic Regression Baseline", 2))
story.append(p("Before training the neural network, a logistic regression model is trained on the same data. This is a linear model: it draws a straight line (or hyperplane in 21 dimensions) to separate the two classes. It serves as the minimum bar the MLP must beat."))
story.append(b("If the MLP cannot beat LR on AUC-ROC, the added complexity is not justified."))
story.append(b("LR is also fully interpretable: each coefficient directly shows how much a feature pushes the prediction toward diabetic or not."))
story.append(p("Result: LR achieved AUC = 0.807 on the test set. The MLP needs to exceed this."))

story.append(sp(8))
story.append(h("Section 3a — Training the MLP", 2))
story.append(p("The MLP is trained using model.fit() with the following setup:"))
story.append(b("50 maximum epochs. Each epoch is one full pass through all 160,631 training rows."))
story.append(b("After each epoch, the model is evaluated on the validation set. The val AUC is tracked."))
story.append(b("Early stopping monitors val AUC. If it does not improve for 5 epochs, training stops and the best weights are restored."))
story.append(b("A CSVLogger saves loss, AUC and accuracy after every epoch to logs/training_log_baseline.csv."))
story.append(sp(4))
story.append(p("Training typically stops around epoch 19-24. The learning curves (loss and AUC vs epoch) are plotted and saved to logs/learning_curves_baseline.png."))

story.append(sp(8))
story.append(h("Section 3b — Overfitting Analysis", 2))
story.append(p("Overfitting means the model has memorised the training data including its noise and cannot generalise. The main indicator is a gap between training and validation performance."))
story.append(two_col_table([
    ["Both loss curves go down together",     "Healthy learning. Model is generalising."],
    ["Train loss down, val loss flat",         "Mild overfitting starting."],
    ["Train loss down, val loss going up",     "Overfitting. Model memorising training data."],
], header=["Learning curve pattern", "Diagnosis"]))
story.append(sp(4))
story.append(p("The gap is also measured numerically by evaluating the model on both train and val sets after training and computing: AUC gap = train AUC - val AUC. A gap above 0.05 indicates significant overfitting."))
story.append(b("Result for the MLP baseline: AUC gap ~0.0008. No significant overfitting detected."))
story.append(b("This is expected: with 160k rows and a shallow 2-layer network, the model does not have enough capacity to memorise the data."))

story.append(sp(8))
story.append(h("Section 3c — Regularization Demonstration", 2))
story.append(p("Even though overfitting is not severe here, three regularisation techniques are demonstrated as required by Loop 3:"))
story.append(b("Early stopping (already in baseline): implicit regularisation. Stops training before the model overfits."))
story.append(b("L2 weight decay (lambda=0.0001): adds a penalty term to the loss equal to lambda times the sum of squared weights. This discourages any weight from becoming very large, which is often a sign of overfitting."))
story.append(b("Dropout (rate=0.3): during each training batch, 30% of neurons are randomly turned off. Each time a different 30% are chosen. This forces the network to not rely on any single neuron and learn more robust representations."))
story.append(sp(4))
story.append(p("All three variants are trained with the same hyperparameters and compared on the test set. The gain is modest here because the baseline already generalises well, but the techniques become critical on deeper or larger models."))

story.append(sp(8))
story.append(h("Section 4 — Decision Threshold Analysis", 2))
story.append(p("The sigmoid output gives a probability between 0 and 1. A threshold converts this to a binary decision: diabetic (1) or not (0). The default threshold of 0.5 is the standard choice but it is not always the right one."))
story.append(sp(4))
story.append(p("In a clinical context the two types of error are not equal:"))
story.append(two_col_table([
    ["False Negative (FN)", "Diabetic patient predicted as healthy. Patient goes undiagnosed. Risk of serious long-term complications. HIGH cost."],
    ["False Positive (FP)", "Healthy patient flagged as diabetic. Patient undergoes unnecessary follow-up. LOW cost."],
], header=["Error type", "Consequence"]))
story.append(sp(4))
story.append(p("Because FN is more costly than FP, we should prefer higher recall (sensitivity) even at the cost of lower precision. Lowering the threshold from 0.5 increases recall."))
story.append(sp(4))
story.append(p("The notebook sweeps thresholds from 0.10 to 0.90 and computes precision, recall, F1 and accuracy at each point. Two thresholds are highlighted:"))
story.append(b("Best F1 threshold (0.25): maximises the balance between precision and recall."))
story.append(b("Clinical threshold (0.15): first threshold achieving recall >= 75%. At this threshold ~82% of diabetic patients are caught, with ~945 missed diagnoses vs ~4,387 at the default 0.5."))
story.append(info_box("The clinical threshold is a proposal that should be validated with Dr. Naye Wells before deployment. The right trade-off between FN and FP is a medical and ethical decision, not just a statistical one.", "#fff8e1"))

story.append(sp(8))
story.append(h("Section 5 — Experiment Tracking", 2))
story.append(p("Every run is logged to logs/experiment_log.json. Each entry contains: run name, timestamp, hyperparameters, architecture description, and all test metrics. If a run is re-executed the old entry is replaced."))
story.append(p("Per-epoch metrics are saved in logs/training_log_*.csv (one file per model variant). This allows plotting training progress for any run at any time."))
story.append(b("4 runs logged: Sprint2_LogisticRegression, Sprint2_MLP_Baseline, Sprint2_MLP_L2, Sprint2_MLP_Dropout."))
story.append(b("The best model (MLP baseline) is saved to models/mlp_baseline.keras and can be reloaded for inference without retraining."))

story.append(sp(8))
story.append(h("Final Results", 2))
story.append(two_col_table([
    ["Logistic Regression", "0.807",  "0.850", "0.238", "4,462"],
    ["MLP Baseline",        "0.815",  "0.854", "0.260", "4,387"],
    ["MLP + L2",            "0.817",  "0.855", "0.262", "4,381"],
    ["MLP + Dropout",       "0.816",  "0.849", "0.047", "5,138"],
], header=["Model", "AUC-ROC", "Accuracy", "F1 (t=0.5)", "FN missed"],
   col_widths=[4.5*cm, 2.5*cm, 2.5*cm, 3*cm, 3.5*cm]))
story.append(sp(4))
story.append(p("At clinical threshold 0.15: MLP Baseline catches ~82% of diabetic patients (recall = 0.82), missing only ~945 out of 5,267 diabetic patients in the test set."))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# CLOSING SECTION
# ═══════════════════════════════════════════════════════════
story.append(h("Observations"))
story.append(hr())
story.append(b("The MLP consistently outperforms logistic regression on AUC-ROC, confirming that non-linear interactions between health features do contribute to prediction. The improvement is modest (~+0.008 AUC) which suggests the non-linear patterns are present but not dominant."))
story.append(b("The class imbalance (85/15) has a strong effect on the default threshold metrics. F1 at threshold 0.5 is very low (~0.26) despite reasonable AUC, because the model defaults toward predicting the majority class."))
story.append(b("Early stopping consistently triggers around epoch 19-24. The learning curves are smooth with no divergence, which is a sign that the architecture and learning rate are well-matched to this dataset."))
story.append(b("L2 regularisation gave the best AUC of the three variants (0.817). Dropout hurt recall at threshold 0.5 significantly, though its AUC was similar to the baseline."))
story.append(b("The train-val AUC gap is near zero for all models. This is unusual and is likely explained by the large dataset size (160k training rows) relative to the model size (3,521 parameters). There is simply too much data for a shallow network to memorise."))
story.append(b("BMI, HighBP and GenHlth are consistently among the top correlates with diabetes. This aligns with medical knowledge."))

story.append(sp(12))
story.append(h("Assumptions"))
story.append(hr())
story.append(b("The BRFSS data is assumed to be representative of the population of interest. It is a telephone survey which may under-represent certain demographics (no phone, language barriers)."))
story.append(b("Pre-diabetes and diabetes are grouped together as class 1. This simplification is stated in the project brief but means the model cannot distinguish between the two conditions."))
story.append(b("The StandardScaler parameters (mean and std) computed on the 2015 training data are assumed to be valid for future data. If patient demographics shift significantly this assumption would fail."))
story.append(b("The 70/15/15 split is assumed to be sufficient for stable evaluation. With 253k rows the test set (34k rows) is large enough to give stable AUC estimates."))
story.append(b("A false negative is assumed to be more clinically costly than a false positive. This is the standard assumption for screening tools but should be confirmed with the medical team."))
story.append(b("Binary and ordinal features are assumed to not require scaling. In practice some ordinal features (e.g. Age with 13 categories) could benefit from scaling but it was kept consistent with the type-based approach."))

story.append(sp(12))
story.append(h("Limitations"))
story.append(hr())
story.append(b("Class imbalance is unaddressed. The 85/15 split is carried through without resampling or class weighting, which limits the model's ability to learn the minority class."))
story.append(b("No hyperparameter search was performed. Layer sizes (64, 32), learning rate (0.001) and batch size (256) were chosen as reasonable defaults, not as optimal values."))
story.append(b("The model is a black box. While AUC is good, the model cannot explain which features drove a particular prediction. This is a concern for clinical deployment and the ethics committee."))
story.append(b("The threshold analysis is done on the test set, which introduces a mild form of test set optimisation. In production the threshold should be set on the validation set only."))
story.append(b("No temporal validation. The data is from a single year (2015). There is no guarantee the model performs well on more recent survey years."))
story.append(b("Environmental cost is not quantified. The notebook trains three models which involves repeated matrix multiplications on 160k rows. The CO2 impact has not been assessed (Loop 4 requirement)."))
story.append(b("Dropout hurt performance at threshold 0.5. At this imbalance ratio, dropout may be removing signal needed to detect the minority class. More investigation is needed."))

story.append(sp(12))
story.append(h("Further Improvements"))
story.append(hr())
story.append(two_col_table([
    ["Class imbalance",        "Apply class_weight={0:1, 1:6} in model.fit() or use SMOTE oversampling to generate synthetic minority class samples."],
    ["Hyperparameter search",  "Use Keras Tuner or sklearn's RandomizedSearchCV to search layer sizes, learning rate, dropout rate and batch size systematically."],
    ["Explainability (SHAP)",  "Compute SHAP values to show which features drove each prediction. Required by the ethics committee for clinical deployment."],
    ["Better threshold",       "Set the clinical threshold on the validation set rather than the test set. Use Youden's J statistic as an objective criterion."],
    ["Deeper architecture",    "Add a third hidden layer (e.g. Dense(128)) and batch normalisation layers to see if a more expressive model improves AUC."],
    ["Feature engineering",    "Create interaction features (e.g. BMI * Age) that the model currently has to discover on its own."],
    ["Environmental tracking", "Use CodeCarbon or similar to log CO2 emissions per training run. Required for Loop 4 compliance."],
    ["Fairness audit",         "Compute performance metrics broken down by Sex, Age and Income groups. Ensure the model does not systematically underperform for vulnerable subgroups (Loop 5)."],
    ["Model calibration",      "Use Platt scaling or isotonic regression to calibrate probabilities so that a prediction of 0.7 actually means 70% chance of diabetes."],
    ["Versioning",             "Use DVC (Data Version Control) or MLflow to version datasets, code and model artefacts together for full reproducibility."],
], header=["Area", "Recommendation"], col_widths=[4*cm, 12*cm]))

story.append(sp(20))
story.append(hr())
story.append(Paragraph("End of Report", style("END","Normal",fontSize=9,textColor=colors.HexColor("#888"),alignment=TA_CENTER)))

# ── Build ────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2.5*cm,
    rightMargin=2.5*cm,
    topMargin=2.5*cm,
    bottomMargin=2.5*cm,
    title="Deep Learning Project Report — Diabetes Prediction",
    author="CESI ETU EN",
)

def first_page(canvas, doc):
    make_cover_footer(canvas, doc)

def later_pages(canvas, doc):
    make_footer(canvas, doc)

doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
print(f"PDF written to: {OUTPUT}")
