# -*- coding: utf-8 -*-
"""
Cloudflight Coding Contest - antrenament - Spy Mission
Level 1: PCA Dimensionality Reduction & Variance Analysis
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

"""Importam setul de date"""

data = pd.read_csv(get_data_path("data.csv"))

"""Standardizam datele"""

scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)

"""Aplicam PCA"""

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

"""Aflam

variatiile (variance) măsoară cât de dispersate sunt valorile unui set de date față de medie

deviatiile (standard deviation) este rădăcina pătrată a variației. Ea are aceeași unitate ca datele originale și arată cât “se abat” valorile în medie față de medie
"""

variances = pca.explained_variance_
std_devs = np.sqrt(variances)
print("Standard deviations:", std_devs.round(2))