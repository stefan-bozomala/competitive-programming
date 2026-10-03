# -*- coding: utf-8 -*-
"""
Cloudflight Coding Contest - 41st Edition (Data/AI)
Level 1: Data Cleaning, Lexical Numeral Parsing, and Multi-key Sorting
Author: Stefan Bozomala
"""

import os
import pandas as pd

# Mapping for textual numerals present in inputs
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

def resolve_path(filename, subfolder="level_1"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        filename,
        os.path.join(script_dir, filename),
        os.path.join(script_dir, "..", "data", subfolder, filename),
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

def process_level_1(input_filename, output_filename=None):
    """
    Reads CSV input, normalizes lexical numerals, removes NaN temperatures,
    and sorts descending by Temperature, ascending by Humidity, ascending by BOP.
    """
    input_path = resolve_path(input_filename, "level_1")
    if not os.path.exists(input_path):
        print(f"[WARN] Fisierul {input_path} nu a fost gasit.")
        return []

    df = pd.read_csv(input_path)

    # Inlocuieste numerele scrise ca text
    df['Temperature [°C]'] = df['Temperature [°C]'].replace(text_to_num)

    # Conversie la numeric si eliminare NaN
    df['Temperature [°C]'] = pd.to_numeric(df['Temperature [°C]'], errors='coerce')
    df = df.dropna(subset=['Temperature [°C]'])

    # Sortare: Temperature descrescator, Humidity crescator, BOP crescator
    df_sorted = df.sort_values(
        by=['Temperature [°C]', 'Humidity [%]', 'BOP'],
        ascending=[False, True, True]
    )

    bop_list = df_sorted['BOP'].astype(int).tolist()

    if output_filename:
        out_path = resolve_output_path(output_filename)
        with open(out_path, "w") as f:
            f.write(" ".join(map(str, bop_list)))
        print(f"[OK] Rezultatul pentru {input_filename} salvat in {out_path} ({len(bop_list)} BOP)")

    return bop_list

if __name__ == "__main__":
    datasets = [
        ("level_1_sample.in", "level_1_sample.txt"),
        ("level_1_a.in", "level_1_a.txt"),
        ("level_1_b.in", "level_1_b.txt"),
        ("level_1_c.in", "level_1_c.txt"),
        ("level_1_d.in", "level_1_d.txt"),
        ("level_1_e.in", "level_1_e.txt")
    ]
    for inp, out in datasets:
        process_level_1(inp, out)