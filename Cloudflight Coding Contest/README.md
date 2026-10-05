# Cloudflight Coding Contest – 41st Edition

My solutions for the **41st Cloudflight Coding Contest (Data & AI Track)**, held on November 14, 2025 in Cluj-Napoca, Romania.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Contest](https://img.shields.io/badge/Cloudflight_CCC-41st_Data%2FAI-purple.svg)](https://cloudflight.io/)

---

## About Me

**Ștefan Bozomala** · UTCN Cluj-Napoca

<!-- Teammates (if any):
- Name Surname · University · GitHub · email
-->

---

## What's in this repo

The contest had two parts — a **practice round** before the event and the **live competition** on the day.

### 🕵️ Practice Round – *Spy Mission*
A multi-level puzzle around a hidden dataset:
- Applied **PCA** to reduce high-dimensional sensor data to 2D
- The scatter plot spelled out a secret password (`metapoint`) hidden in the point positions
- Cleaned noisy data (missing values, out-of-range readings)
- Converted temperature units and computed basic statistics

### 🐦 Live Competition – *Bird Love Score*
Predict an ecological habitability score for bird habitats:
- Parsed and cleaned messy field data (numbers written as English words, mixed units, corrupted rows)
- Merged data from multiple sources and fixed Fahrenheit/Celsius mix-ups
- Trained a **neural network** to predict missing "Bird Love Score" values

---

## Results

| Round | Task | Outcome |
|---|---|---|
| Practice | Hidden password in scatter plot | Found: `metapoint` ✅ |
| Practice | Data cleaning | 971 valid rows kept out of 1000 ✅ |
| Live | BOP habitat sorting | Validated outputs ✅ |
| Live | Bird Love Score prediction | Submitted for datasets B & C ✅ |

---

## Repo Structure

```
├── 01-practice-spy-mission/   # Practice round scripts & data
│   └── src/                   # lvl1.py → lvl4.py
├── 02-competition-41st-ccc/   # Live competition scripts & data
│   └── src/                   # NIVEL1.py, varianta_finala_de_cod.py
├── docs/                      # Participation certificate & event photos
└── requirements.txt
```

---

## Running the Code

```bash
# Setup
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Practice round
python 01-practice-spy-mission/src/lvl1.py   # PCA
python 01-practice-spy-mission/src/lvl2.py   # Password visualization
python 01-practice-spy-mission/src/lvl3.py   # Data cleaning
python 01-practice-spy-mission/src/lvl4.py   # Temperature stats

# Live competition
python 02-competition-41st-ccc/src/NIVEL1.py
python 02-competition-41st-ccc/src/varianta_finala_de_cod.py
```

---

*Organized by [Cloudflight GmbH](https://cloudflight.io/coding-contest/) · Venue: CREIC, Cluj-Napoca*
