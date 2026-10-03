# -*- coding: utf-8 -*-
"""
Cloudflight Coding Contest - antrenament - Spy Mission
Level 3: Missing Value Imputation/Removal & Outlier Filtering
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    import tensorflow as tf
except ImportError:
    tf = None

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def get_data_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        filename,
        os.path.join(script_dir, filename),
        os.path.join(script_dir, "..", "data", filename),
        os.path.join(script_dir, "..", "..", "01-practice-spy-mission", "data", filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return filename

"""##Nivel 3
Citim csv - train
"""

train_path = get_data_path("train_data.csv")
train = pd.read_csv(train_path)

print(f"Numar initial de randuri in {os.path.basename(train_path)}: {len(train)}")

"""Gasim si eliminam randurile cu NOT-A-NUMBER"""

print("\nColoane cu NaN:")
print(train.isna().sum())

train = train.dropna()
print(f"Randuri dupa dropna: {len(train)}")

"""Gasim si eliminam OUTLIERS conform specificatiilor din level_3.pdf:
- AMPS in [0, 1]
- VOLTS in [0.02, 8.7]
- TEMP in [-100, 373.15]
- DELTA in [-1, 1]
- GAMMA in [-2, 2]
- OUTPUT in [-8.4, 9.3]
"""

train = train[(train['AMPS'] >= 0) & (train['AMPS'] <= 1)]
train = train[(train['VOLTS'] >= 0.02) & (train['VOLTS'] <= 8.7)]
train = train[(train['TEMP'] >= -100) & (train['TEMP'] <= 373.15)]
train = train[(train['DELTA'] >= -1) & (train['DELTA'] <= 1)]
train = train[(train['GAMMA'] >= -2) & (train['GAMMA'] <= 2)]
train = train[(train['OUTPUT'] >= -8.4) & (train['OUTPUT'] <= 9.3)]

"""Numarul de randuri ramase"""

print(f"\nNumarul final de randuri valide ramase: {len(train)}")