# -*- coding: utf-8 -*-
"""
Cloudflight Coding Contest - 41st Edition (Data/AI)
VARIANTA FINALA DE COD: Pipeline complet pentru Nivelul 1 si Nivelul 2 (Neural Regression)
Autor: Stefan Bozomala
Competitie: 41st Data/AI CCC 2025 (CREIC Cluj-Napoca)
"""

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Incercam importul TensorFlow/Keras; daca nu este disponibil, folosim PyTorch
USE_TF = False
try:
    import tensorflow as tf
    USE_TF = True
except ImportError:
    import torch
    import torch.nn as nn

# Dictionar pentru maparea numerelor scrise ca text
text_to_num = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20, "twenty-one": 21,
    "twenty-two": 22, "twenty-three": 23, "twenty-four": 24,
    "twenty-five": 25, "twenty-six": 26, "twenty-seven": 27,
    "twenty-eight": 28, "twenty-nine": 29, "thirty": 30,
    "thirty-one": 31, "thirty-two": 32, "thirty-three": 33,
    "thirty-four": 34
}

def resolve_path(filename, subfolder="level_2"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        filename,
        os.path.join(script_dir, filename),
        os.path.join(script_dir, "..", "data", subfolder, filename),
        os.path.join(script_dir, "..", "data", "level_1", filename),
        os.path.join(script_dir, "..", "..", "02-competition-41st-ccc", "data", subfolder, filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return filename

def resolve_output_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(script_dir, "..", "data", "results")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, filename)

def fahrenheit_to_celsius(temp):
    """Euristica: temperaturile > 60 sunt considerate exprimate in Fahrenheit"""
    if temp > 60:
        return (temp - 32) * 5 / 9
    return temp

def move_column_to_end(df, col):
    cols = list(df.columns)
    cols.append(cols.pop(cols.index(col)))
    return df[cols]

# ==============================================================================
# NIVEL 1 - Functie rezolvare seturi de date
# ==============================================================================
def run_level_1():
    print("=" * 60)
    print("EXECUTARE PIPELINE NIVEL 1")
    print("=" * 60)
    files = ["level_1_sample.in", "level_1_a.in", "level_1_b.in", "level_1_c.in", "level_1_d.in", "level_1_e.in"]
    for fname in files:
        fpath = resolve_path(fname, "level_1")
        if not os.path.exists(fpath):
            continue
        df = pd.read_csv(fpath)
        df['Temperature [°C]'] = df['Temperature [°C]'].replace(text_to_num)
        df['Temperature [°C]'] = pd.to_numeric(df['Temperature [°C]'], errors='coerce')
        df = df.dropna(subset=['Temperature [°C]'])
        df_sorted = df.sort_values(
            by=['Temperature [°C]', 'Humidity [%]', 'BOP'],
            ascending=[False, True, True]
        )
        bop_list = df_sorted['BOP'].astype(int).tolist()
        out_name = fname.replace(".in", ".txt")
        out_path = resolve_output_path(out_name)
        with open(out_path, "w") as f:
            f.write(" ".join(map(str, bop_list)))
        print(f"[NIVEL 1] {fname} -> {out_name} ({len(bop_list)} BOP)")

# ==============================================================================
# NIVEL 2 - Antrenare Retea Neuronala & Predictie Bird Love Score
# ==============================================================================
def train_and_predict_ann(train_csv_name, predict_csv_name, output_csv_name):
    print("=" * 60)
    print(f"EXECUTARE PIPELINE NIVEL 2: Predictie pentru {predict_csv_name}")
    print("=" * 60)

    # 1. Citire si preprocesare all_data_from_level_1
    df_temp_path = resolve_path("all_data_from_level_1.in", "level_2")
    df_temp = pd.read_csv(df_temp_path)
    df_temp['Temperature [°C]'] = df_temp['Temperature [°C]'].replace({'seventeen': 17})
    df_temp['Temperature [°C]'] = pd.to_numeric(df_temp['Temperature [°C]'], errors='coerce')
    df_temp['Temperature [°C]'] = df_temp['Temperature [°C]'].apply(fahrenheit_to_celsius)

    # 2. Citire fisier de antrenare (de ex. level_2_b.in)
    train_file_path = resolve_path(train_csv_name, "level_2")
    df_train_in = pd.read_csv(train_file_path)

    # Merge pe cheia primara 'BOP'
    df_merged = pd.merge(df_temp, df_train_in, on='BOP', how='inner')
    df_merged = move_column_to_end(df_merged, 'Bird Love Score [<3]')

    # Separare inregistrari cu eticheta cunoscuta vs 'missing'
    df_train_valid = df_merged[df_merged['Bird Love Score [<3]'] != 'missing'].copy()

    X_train_raw = df_train_valid.drop(columns=['Bird Love Score [<3]']).values.astype(np.float32)
    y_train = df_train_valid['Bird Love Score [<3]'].values.astype(np.float32).reshape(-1, 1)

    # Scalare date
    sc = StandardScaler()
    X_train_scaled = sc.fit_transform(X_train_raw)

    # 3. Antrenare model retea neuronala (ANN / MLP)
    if USE_TF:
        print("[INFO] Folosire runtime TensorFlow/Keras...")
        ann = tf.keras.models.Sequential([
            tf.keras.layers.Dense(units=128, activation=tf.keras.layers.LeakyReLU(negative_slope=0.01)),
            tf.keras.layers.Dense(units=64, activation=tf.keras.layers.LeakyReLU(negative_slope=0.01)),
            tf.keras.layers.Dense(units=64, activation=tf.keras.layers.LeakyReLU(negative_slope=0.01)),
            tf.keras.layers.Dense(units=32, activation=tf.keras.layers.LeakyReLU(negative_slope=0.01)),
            tf.keras.layers.Dense(units=16, activation=tf.keras.layers.LeakyReLU(negative_slope=0.01)),
            tf.keras.layers.Dense(units=4, activation=tf.keras.layers.LeakyReLU(negative_slope=0.01)),
            tf.keras.layers.Dense(units=1)
        ])
        ann.compile(optimizer='adam', loss='mse', metrics=[tf.keras.metrics.RootMeanSquaredError()])
        ann.fit(X_train_scaled, y_train, batch_size=32, epochs=100, verbose=0)
    else:
        print("[INFO] Folosire runtime PyTorch (arhitectura identica)...")
        in_features = X_train_scaled.shape[1]
        model = nn.Sequential(
            nn.Linear(in_features, 128), nn.LeakyReLU(0.01),
            nn.Linear(128, 64), nn.LeakyReLU(0.01),
            nn.Linear(64, 64), nn.LeakyReLU(0.01),
            nn.Linear(64, 32), nn.LeakyReLU(0.01),
            nn.Linear(32, 16), nn.LeakyReLU(0.01),
            nn.Linear(16, 4), nn.LeakyReLU(0.01),
            nn.Linear(4, 1)
        )
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
        X_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
        y_tensor = torch.tensor(y_train, dtype=torch.float32)

        for _ in range(100):
            optimizer.zero_grad()
            out = model(X_tensor)
            loss = criterion(out, y_tensor)
            loss.backward()
            optimizer.step()

    # 4. Predictie pentru setul tinta
    target_file_path = resolve_path(predict_csv_name, "level_2")
    df_target_in = pd.read_csv(target_file_path)
    df_target_merged = pd.merge(df_temp, df_target_in, on='BOP', how='inner')
    df_target_missing = df_target_merged[df_target_merged['Bird Love Score [<3]'] == 'missing'].copy()

    if len(df_target_missing) == 0:
        df_target_missing = df_target_merged.copy()

    X_target = df_target_missing.drop(columns=['Bird Love Score [<3]']).values.astype(np.float32)
    X_target_scaled = sc.transform(X_target)

    if USE_TF:
        y_pred = ann.predict(X_target_scaled, verbose=0).flatten()
    else:
        model.eval()
        with torch.no_grad():
            y_pred = model(torch.tensor(X_target_scaled, dtype=torch.float32)).numpy().flatten()

    df_out = pd.DataFrame({
        'BOP': df_target_missing['BOP'].values,
        'Bird Love Score [<3]': y_pred
    })

    out_file = resolve_output_path(output_csv_name)
    df_out.to_csv(out_file, index=False)
    print(f"[NIVEL 2] Predictii generate cu succes in {out_file} ({len(df_out)} randuri)")
    return df_out

if __name__ == "__main__":
    run_level_1()
    # Generare predictii pentru Level 2 (B si C)
    train_and_predict_ann("level_2_b.in", "level_2_b.in", "raspuns_b.csv")
    train_and_predict_ann("level_2_b.in", "level_2_c.in", "raspuns_c.csv")