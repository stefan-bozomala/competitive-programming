# Cloudflight Coding Contest: AI Spy Mission (Practice Track)

This module contains the solutions and data pipeline for the practice track **"AI: Spy Mission"** in the Cloudflight Coding Contest (Data & AI Track).

---

## Challenge Summary

The challenge revolves around a cyber-investigation scenario. An encrypted archive and a CSV dataset (`data.csv`) were found on a confiscated USB drive. The goal is to uncover the password, clean the decrypted dataset, and standardize physical measurement units.

### Levels Overview

| Level | Objective | Approach | Key Result |
|---|---|---|---|
| **Level 1** | Inspect data & reduce dimensions | `StandardScaler` + `PCA(n_components=2)` | Standard deviations: `[1.97, 1.00]` |
| **Level 2** | Recover the hidden password | 2D Scatter Plot + invert Y axis | Password: `"metapoint"` |
| **Level 3** | Clean missing values & outliers | Drop `NaN` + filter sensor intervals | `971` valid rows (from 1000) |
| **Level 4** | Convert temperature units | Convert Kelvin to Celsius ($T_C = T_K - 273.15$) | Mean: `-0.69°C`, Std: `48°C` |

---

## How Each Level Works

### Level 1: PCA Dimensionality Reduction (`src/lvl1.py`)
- Reads `data/data.csv`.
- Scales features using scikit-learn's `StandardScaler`.
- Fits a 2-component PCA to compute the standard deviations of the principal components (`sqrt(explained_variance_)`).

### Level 2: Steganographic Password Recovery (`src/lvl2.py`)
- Projects the data into the 2D principal component space.
- Inverting the vertical coordinate (`PC2 = -PC2`) reveals the word **`metapoint`** spelled out by the points in the scatter plot.
- This password unlocks `encrypted.zip` in `data/archives/`, which contains `train_data.csv` and `test_data.csv`.
- The script automatically saves the visualization to `figures/pca_metapoint_scatter.png`.

### Level 3: Data Cleaning & Outlier Rejection (`src/lvl3.py`)
- Loads `data/train_data.csv`.
- Drops rows containing `NaN` (16 rows removed).
- Filters rows outside the specified sensor intervals (13 rows removed):
  - `AMPS` in `[0, 1]`
  - `VOLTS` in `[0.02, 8.7]`
  - `TEMP` in `[-100, 373.15]`
  - `DELTA` in `[-1, 1]`
  - `GAMMA` in `[-2, 2]`
  - `OUTPUT` in `[-8.4, 9.3]`
- Output: 971 valid rows remaining.

### Level 4: Kelvin to Celsius Conversion (`src/lvl4.py`)
- Isolates records where `UNIT == 'K'`.
- Converts values to Celsius by subtracting 273.15.
- Computes the mean (`-0.69°C`) and standard deviation (`48°C`) across all 221 Kelvin readings.

---

## Directory Structure

```text
01-practice-spy-mission/
├── docs/                      # Problem statements (PDFs for Levels 1–4)
│   ├── level_1.pdf
│   ├── level_2.pdf
│   ├── level_3.pdf
│   └── level_4.pdf
├── data/                      # Datasets & contest archives
│   ├── data.csv
│   ├── train_data.csv
│   ├── test_data.csv
│   └── archives/
│       ├── input.zip
│       └── encrypted.zip      # Unlocked with password: metapoint
├── figures/                   # Generated scatter plots
│   └── pca_metapoint_scatter.png
└── src/                       # Python solution scripts
    ├── lvl1.py
    ├── lvl2.py
    ├── lvl3.py
    └── lvl4.py
```

---

## Running the Scripts

Run from the repository root:

```bash
# Level 1
python 01-practice-spy-mission/src/lvl1.py

# Level 2 (saves figure to figures/pca_metapoint_scatter.png)
python 01-practice-spy-mission/src/lvl2.py

# Level 3
python 01-practice-spy-mission/src/lvl3.py

# Level 4
python 01-practice-spy-mission/src/lvl4.py
```
