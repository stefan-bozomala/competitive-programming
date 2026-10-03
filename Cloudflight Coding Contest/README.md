# Cloudflight Coding Contest (CCC) – 41st Edition: Data & AI Track

Solutions, data pipelines, and machine learning models developed for the **41st Cloudflight Coding Contest (Data & AI Track)**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red.svg)](https://pytorch.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15%2B-FF6F00.svg)](https://www.tensorflow.org/)
[![Contest](https://img.shields.io/badge/Cloudflight_CCC-41st_Data%2FAI-purple.svg)](https://cloudflight.io/)

---

## Participant & Event Info

- **Participant:** **Ștefan Bozomală**
- **University:** Technical University of Cluj-Napoca (UTCN), Romania
- **Event:** 41st Cloudflight Coding Contest (Data & AI Track)
- **Date:** November 14, 2025
- **Location:** CREIC – Regional Centre of Excellence for Creative Industries, Cluj-Napoca, Romania
- **Organizer:** Cloudflight GmbH
- **Participation Certificate:** [`docs/ccc-participation-certificate-41st-data-ai-ccc-2025-5774.pdf`](docs/ccc-participation-certificate-41st-data-ai-ccc-2025-5774.pdf) (Certificate ID: `#5774`)

---

## Overview

This repository contains the complete code, datasets, problem statements, and results for both the practice track and the official live competition:

### 1. Practice Track: *AI: Spy Mission*
- **Level 1 (PCA Dimensionality Reduction):** Standardized high-dimensional sensor data and applied Principal Component Analysis (PCA) to reduce it to 2 dimensions, computing component standard deviations.
- **Level 2 (Visual Password Recovery):** Plotted the 2D PCA projection as a scatter plot. Inverting the axes reveals a hidden word written by the points: **`metapoint`**, which serves as the password to unlock `encrypted.zip`.
- **Level 3 (Data Cleaning & Outlier Removal):** Removed rows with missing values (`NaN`) and filtered sensor measurements outside valid physical ranges.
- **Level 4 (Temperature Conversion & Statistics):** Converted temperature values from Kelvin to Celsius and computed summary statistics (mean and standard deviation).

### 2. Live Competition: *Ecological Habitability – Bird Love Score*
- **Level 1 (Data Cleaning & Compound Sorting):**
  - Cleaned microclimate habitat observations (`BOP`, `Temperature`, `Humidity`).
  - Handled numbers written as English words (e.g., `"seventeen"` $\to$ `17`).
  - Filtered corrupted values and sorted rows by **Temperature** (descending), **Humidity** (ascending), and **BOP ID** (ascending).
- **Level 2 (Multi-Source Fusion & Neural Network Regression):**
  - Merged climate data from Level 1 with environmental features from Level 2 (`Vegetation`, `Insects`, `Urban Light`).
  - Corrected temperatures erroneously recorded in Fahrenheit (> 60°F) to Celsius.
  - Trained a deep Artificial Neural Network (ANN) regression model with LeakyReLU activations and Adam optimizer to predict the missing `Bird Love Score [<3]` target values.

---

## Repository Structure

```text
cloudflight-coding-contest-41/
├── .gitignore                          # Exclusions for Python caches, virtualenvs, IDEs
├── README.md                           # Project documentation
├── requirements.txt                    # Project dependencies
├── docs/                               # Official certificates and contest photos
│   ├── ccc-participation-certificate-41st-data-ai-ccc-2025-5774.pdf  # CCC Certificate #5774
│   └── assets/
│       └── 20251113_200006.jpg         # Photo of the PCA scatter plot on screen
├── 01-practice-spy-mission/            # Practice Track: "AI: Spy Mission"
│   ├── README.md                       # Track overview
│   ├── docs/                           # Problem statements (PDFs for Levels 1–4)
│   ├── data/                           # Data files (data.csv, train_data.csv, test_data.csv)
│   │   └── archives/                   # input.zip, encrypted.zip (password: metapoint)
│   ├── figures/                        # Generated scatter plot showing "metapoint"
│   │   └── pca_metapoint_scatter.png
│   └── src/                            # Solution scripts
│       ├── lvl1.py                     # PCA & standard deviation computation
│       ├── lvl2.py                     # 2D projection & password visualization
│       ├── lvl3.py                     # Missing values & outlier cleaning
│       └── lvl4.py                     # Kelvin to Celsius conversion & stats
└── 02-competition-41st-ccc/            # Live Competition: 41st CCC
    ├── README.md                       # Track overview
    ├── data/
    │   ├── level_1/                    # Level 1 inputs (a, b, c, d, e, sample)
    │   ├── level_2/                    # Level 2 inputs & merged level 1 data
    │   ├── archives/                   # level_1.zip, level_2.zip
    │   └── results/                    # Validated output solutions (CSV / TXT)
    │       ├── level_1_c.txt           # Sorted BOP sequence
    │       ├── raspuns_b.csv           # Model predictions for test set B
    │       └── raspuns_c.csv           # Model predictions for test set C
    └── src/                            # Solution scripts
        ├── NIVEL1.py                   # Level 1 data cleaning & multi-key sorting
        └── varianta_finala_de_cod.py   # Full pipeline (Level 1 + ANN regression for Level 2)
```

---

## How the Solutions Work

### 1. Spy Mission Pipeline
1. **PCA (`lvl1.py`):** Uses `StandardScaler` to normalize the feature space, then fits a 2-component `PCA`. The resulting component standard deviations are `[1.97, 1.00]`.
2. **Password Recovery (`lvl2.py`):** Inverting the vertical axis (`PC2 = -PC2`) reveals the steganographic word **`metapoint`** spelled out by the scatter points. This unlocks `encrypted.zip` containing `train_data.csv` and `test_data.csv`.
3. **Data Cleaning (`lvl3.py`):** Drops `NaN` entries (16 rows) and removes readings outside physical sensor bounds (13 rows), leaving 971 valid rows out of 1000:
   - `AMPS` in `[0, 1]`
   - `VOLTS` in `[0.02, 8.7]`
   - `TEMP` in `[-100, 373.15]`
   - `DELTA` in `[-1, 1]`
   - `GAMMA` in `[-2, 2]`
   - `OUTPUT` in `[-8.4, 9.3]`
4. **Unit Conversion (`lvl4.py`):** Converts Kelvin temperatures to Celsius ($T_C = T_K - 273.15$). The resulting 221 converted readings have a mean of `-0.69°C` and a standard deviation of `48°C`.

### 2. Live Competition Pipeline
1. **Lexical Parsing & Sorting (`NIVEL1.py`):**
   - Replaces written English numbers (e.g., `'seventeen' -> 17`).
   - Drops invalid/NaN temperature entries.
   - Sorts records by: `Temperature` (descending), `Humidity` (ascending), `BOP` (ascending).
   - Extracts the sorted list of BOP IDs into space-separated text files.
2. **Neural Network Regression (`varianta_finala_de_cod.py`):**
   - Merges Level 1 temperature and humidity with Level 2 features (`Vegetation`, `Insects`, `Urban Light`) on `BOP`.
   - Normalizes temperatures recorded in Fahrenheit (> 60°F) to Celsius: $T_C = (T_F - 32) \times 5/9$.
   - Trains a deep feedforward neural network (ANN) with LeakyReLU activations ($\alpha = 0.01$) to predict the missing `Bird Love Score [<3]`:
     ```text
     Input (5 features) -> Dense(128) -> Dense(64) -> Dense(64) -> Dense(32) -> Dense(16) -> Dense(4) -> Dense(1)
     ```
   - Automatically supports both **TensorFlow/Keras** and **PyTorch** runtimes.

---

## Results Summary

| Track | Level | Objective | Result / Key Output |
|---|---|---|---|
| **Practice** | Level 1 | PCA standard deviations | `[1.97, 1.00]` |
| **Practice** | Level 2 | Hidden password recovery | `metapoint` (unlocks `encrypted.zip`) |
| **Practice** | Level 3 | Valid rows after cleaning | `971` rows (from 1000) |
| **Practice** | Level 4 | Kelvin to Celsius stats | Mean: `-0.69°C`, Std: `48°C` |
| **Live CCC** | Level 1 | Sorted BOP sequence | Validated outputs (`level_1_*.txt`) |
| **Live CCC** | Level 2 | Predicted Bird Love Score | `raspuns_b.csv` (200 rows), `raspuns_c.csv` (100 rows) |

---

## Quickstart & Execution

### 1. Setup Environment

```bash
# Clone the repository
git clone https://github.com/BozomalaStefan-30126/cloudflight-coding-contest-41.git
cd cloudflight-coding-contest-41

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
# source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Practice Track Scripts

```bash
# Level 1: PCA standard deviations
python 01-practice-spy-mission/src/lvl1.py

# Level 2: Generate 2D scatter plot (saves figure to figures/)
python 01-practice-spy-mission/src/lvl2.py

# Level 3: Clean data and filter outliers
python 01-practice-spy-mission/src/lvl3.py

# Level 4: Temperature conversion and statistics
python 01-practice-spy-mission/src/lvl4.py
```

### 3. Run Live Competition Scripts

```bash
# Level 1: Process all input batches (sample, a, b, c, d, e)
python 02-competition-41st-ccc/src/NIVEL1.py

# Full Pipeline: Level 1 + Level 2 Neural Network Regression
python 02-competition-41st-ccc/src/varianta_finala_de_cod.py
```

---

## Acknowledgements

- **Organizer:** [Cloudflight GmbH](https://cloudflight.io/coding-contest/)
- **Contest Platform:** [codingcontest.org](https://codingcontest.org/)
- **Venue:** CREIC – Regional Centre of Excellence for Creative Industries, Cluj-Napoca, Romania
- **Affiliation:** Technical University of Cluj-Napoca (UTCN)
