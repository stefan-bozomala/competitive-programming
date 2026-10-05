# Cloudflight Coding Contest – 41st Edition (Data & AI Track)

Solutions developed for the **41st Cloudflight Coding Contest**, Data & AI track, held on **November 14, 2025** in Cluj-Napoca, Romania.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red.svg)](https://pytorch.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15%2B-FF6F00.svg)](https://www.tensorflow.org/)
[![Contest](https://img.shields.io/badge/Cloudflight_CCC-41st_Data%2FAI-purple.svg)](https://cloudflight.io/)

---

## Participant

**Ștefan Bozomala** · Technical University of Cluj-Napoca (UTCN) · 📄 [Participation Certificate](docs/ccc-participation-certificate-41st-data-ai-ccc-2025-5774.pdf)

- Teammates:
 Bianca Anechitei · Technical University of Cluj-Napoca
 Sebastian Pereni · Technical University of Cluj-Napoca

---

## The Contest

CCC is a timed coding competition where teams solve progressively harder data/ML problems under time pressure. This edition included two tracks: a **practice round** available before the event, and the actual **live competition**.

---

## Practice Round – *AI: Spy Mission*

A 4-level challenge built around a hidden dataset that needed to be unlocked step by step.

| Level | Task | Approach |
|---|---|---|
| 1 | Reduce high-dimensional sensor data | PCA with `StandardScaler` → 2 components |
| 2 | Recover a hidden password from the data | Plotting the 2D projection (with inverted Y-axis) reveals the word **`metapoint`** written by the point cloud |
| 3 | Clean a corrupted sensor dataset | Dropped NaN rows + filtered readings outside valid physical ranges → 971/1000 rows kept |
| 4 | Temperature conversion + stats | Kelvin → Celsius conversion; computed mean (`-0.69°C`) and std (`48°C`) |

---

## Live Competition – *Ecological Habitability: Bird Love Score*

Predict a habitability score for bird habitats based on microclimate and environmental features.

### Level 1 — Data Cleaning & Sorting
- Input data had numbers written as English words (e.g. `"seventeen"`) — parsed these programmatically
- Dropped corrupted/missing temperature entries
- Sorted habitat observations by Temperature (desc), Humidity (asc), and BOP ID (asc)

### Level 2 — Feature Fusion & Neural Network Regression
- Merged Level 1 climate data with Level 2 environmental features (Vegetation, Insects, Urban Light)
- Detected and corrected temperatures recorded in Fahrenheit instead of Celsius
- Trained a deep feedforward **ANN** (5 inputs → 7 hidden layers → 1 output) with LeakyReLU activations and Adam optimizer to predict the missing `Bird Love Score` target
- Model automatically adapts to run on either **TensorFlow/Keras** or **PyTorch**

---

## Results

| Round | Level | Outcome |
|---|---|---|
| Practice | 1 – PCA | Component std devs: `[1.97, 1.00]` ✅ |
| Practice | 2 – Password recovery | `metapoint` — unlocked `encrypted.zip` ✅ |
| Practice | 3 – Data cleaning | 971 valid rows out of 1000 ✅ |
| Practice | 4 – Temperature stats | Mean: `-0.69°C`, Std: `48°C` ✅ |
| Live CCC | 1 – BOP sorting | Validated outputs for all batches ✅ |
| Live CCC | 2 – Bird Love Score | Predictions submitted for datasets B & C ✅ |

---

## Repository Structure

```
├── 01-practice-spy-mission/
│   ├── src/                  # lvl1.py → lvl4.py (one script per level)
│   ├── data/                 # input.zip, encrypted.zip (password: metapoint)
│   └── figures/              # Generated scatter plot revealing the password
├── 02-competition-41st-ccc/
│   ├── src/
│   │   ├── NIVEL1.py                     # Data cleaning & sorting
│   │   └── varianta_finala_de_cod.py     # Full Level 1 + Level 2 ANN pipeline
│   ├── data/                             # Input batches (a–e) and result CSVs
│   └── data/results/                     # Validated output files
├── docs/                     # Participation certificate + event photos
└── requirements.txt
```

---

## Quickstart

```bash
git clone https://github.com/BozomalaStefan-30126/cloudflight-coding-contest-41.git
cd cloudflight-coding-contest-41

python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows
# source .venv/bin/activate       # Linux/macOS
pip install -r requirements.txt

# Practice round
python 01-practice-spy-mission/src/lvl1.py
python 01-practice-spy-mission/src/lvl2.py
python 01-practice-spy-mission/src/lvl3.py
python 01-practice-spy-mission/src/lvl4.py

# Live competition
python 02-competition-41st-ccc/src/NIVEL1.py
python 02-competition-41st-ccc/src/varianta_finala_de_cod.py
```

---

*Organized by [Cloudflight GmbH](https://cloudflight.io/coding-contest/) · Venue: CREIC, Cluj-Napoca, Romania*
