# -*- coding: utf-8 -*-
"""
Cloudflight Coding Contest - antrenament - Spy Mission
Level 2: 2D Scatter Plot & Steganographic Password Recovery ("metapoint")
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

"""##Nivel 1
Importam setul de date
"""

data = pd.read_csv(get_data_path("data.csv"))

"""Standardizam datele"""

scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)

"""Aplicam PCA"""

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

"""Aflam
variatiile (variance) si deviatiile (standard deviation)
"""

variances = pca.explained_variance_
std_devs = np.sqrt(variances)
print("Standard deviations:", std_devs.round(2))

"""##Nivel 2

2D scatter plot
Cream un DataFrame cu rezultatele
"""

pca_df = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])

"""Scatter Plot"""

pca_df['PC2'] = -pca_df['PC2']  # rasturnam graficul pe axa Y
# Nota: inversand si PC1 (pca_df['PC1'] = -pca_df['PC1']) textul se citeste direct de la stanga la dreapta: 'metapoint'

fig = plt.figure(figsize=(15, 5))
plt.scatter(
    pca_df['PC1'], pca_df['PC2'],
    c='blue',
    s=30,          # dimensiunea punctelor
    alpha=1,       # transparenta
    edgecolors='k' # contur negru subtire
)

plt.xlabel('Componenta principala 1')
plt.ylabel('Componenta principala 2')
plt.title('Proiectia PCA in 2D (Parola ascunsa: metapoint)')
plt.grid(True)

# Salveaza automat figura in folderul de output
output_fig_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures", "pca_metapoint_scatter.png")
os.makedirs(os.path.dirname(output_fig_path), exist_ok=True)
plt.savefig(output_fig_path, dpi=200, bbox_inches='tight')
print(f"Graficul a fost salvat in: {output_fig_path}")
if os.environ.get("SHOW_PLOTS", "0") == "1":
    plt.show()
else:
    plt.close()

"""CE TARE E CHESTIA ASTA - rasucim invers si rotim => metapoint - parola de la seturile de training si test"""