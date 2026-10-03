# -*- coding: utf-8 -*-
"""
Cloudflight Coding Contest - antrenament - Spy Mission
Level 4: Unit Conversion & Statistical Feature Normalization (Kelvin -> Celsius)
"""

import os
import numpy as np
import pandas as pd

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

"""##Nivel 3 - Curatare NaN si Outliers"""

train_path = get_data_path("train_data.csv")
train = pd.read_csv(train_path)

# Eliminare NaN
train = train.dropna()

# Eliminare Outliers
train = train[(train['AMPS'] >= 0) & (train['AMPS'] <= 1)]
train = train[(train['VOLTS'] >= 0.02) & (train['VOLTS'] <= 8.7)]
train = train[(train['TEMP'] >= -100) & (train['TEMP'] <= 373.15)]
train = train[(train['DELTA'] >= -1) & (train['DELTA'] <= 1)]
train = train[(train['GAMMA'] >= -2) & (train['GAMMA'] <= 2)]
train = train[(train['OUTPUT'] >= -8.4) & (train['OUTPUT'] <= 9.3)]

"""##Nivel 4 - Conversie Kelvin -> Celsius
Calculam media si deviatia standard a valorilor transformate din K in °C
"""

# Extragem valorile a caror unitate de masura este 'K'
kelvin = train[train['UNIT'] == 'K']['TEMP']

# Transformare in grade Celsius: T_C = T_K - 273.15
kelvin_c = kelvin - 273.15

# Calcul medie si deviatie standard la nivel de populatie (ddof=0)
mean_c = round(kelvin_c.mean(), 2)
std_c = round(kelvin_c.std(ddof=0), 0)

print(f"Numar inregistrari in Kelvin: {len(kelvin)}")
print(f"Mean (°C): {mean_c}")
print(f"Standard deviation (°C): {int(std_c)}")