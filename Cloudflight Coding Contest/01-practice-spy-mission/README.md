# Cloudflight Coding Contest: AI Spy Mission (Practice Track)

This module contains the complete analytic pipelines and algorithmic solutions for the practice round **"AI: Spy Mission"** in the Cloudflight Coding Contest (Data & AI Track).

---

## 1. Problem Formulation & Task Architecture

The analytical scenario positions the researcher as a data analyst within a cyber-intelligence unit. A confiscated USB device contained an encrypted archive and a seemingly random high-dimensional dataset (`data.csv`). The objective is to retrieve access credentials via unsupervised feature projection (PCA), decrypt the protected archive, filter missing values and sensor anomalies (outliers), and standardize thermodynamic measurement units.

### Levels and Objectives

| Level | Title | Method / Framework | Key Output |
|---|---|---|---|
| **Level 1** | *Data Inspection & Dimensionality Reduction* | StandardScaler + PCA ($D \to 2$) | Standard deviations: `[1.97, 1.00]` |
| **Level 2** | *Steganographic Password Retrieval* | 2D Scatter Plot + Coordinate Inversion | Extracted password: `"metapoint"` |
| **Level 3** | *Data Cleansing & Anomaly Rejection* | NaN Dropping + Physical Domain Bounding | Valid rows: `971` (out of 1000) |
| **Level 4** | *Thermodynamic Normalization (K $\to$ °C)* | Affine Transform $T_C = T_K - 273.15$ | $\mu = -0.69^\circ\text{C}$, $\sigma = 48^\circ\text{C}$ |

---

## 2. Mathematical Modeling

### Level 1: Principal Component Analysis (PCA)
Given observation matrix $X \in \mathbb{R}^{N \times D}$, features are centered and standardized to unit variance:
$$Z = \frac{X - \mu_X}{\sigma_X}$$
The sample covariance matrix $\Sigma$:
$$\Sigma = \frac{1}{N - 1} Z^T Z$$
By spectral decomposition or SVD ($Z = U S V^T$):
$$\Sigma v_i = \lambda_i v_i$$
where $\lambda_i$ denotes the explained variance of principal component $i$, with corresponding standard deviation:
$$\sigma_i = \sqrt{\lambda_i} = \frac{S_i}{\sqrt{N - 1}}$$

### Level 2: Steganographic Password Recovery
Projecting data points onto the top two principal eigenvectors:
$$Z_{2D} = Z \cdot [v_1, v_2]$$
Applying a parity reflection across coordinates:
$$(x', y') = (-x, -y)$$
visually uncovers the Latin keyword **`metapoint`**, representing the encryption key for `encrypted.zip`.

### Level 3: Bounded Physical Domain Filtering
Samples are retained if and only if they contain no `NaN` values and strictly lie within physical transducer boundaries:
$$\mathcal{D} = \left\{ x \in \mathbb{R}^k \ \middle|\ 
\begin{array}{l}
\text{AMPS} \in [0, 1], \quad \text{VOLTS} \in [0.02, 8.7], \\
\text{TEMP} \in [-100, 373.15], \quad \text{DELTA} \in [-1, 1], \\
\text{GAMMA} \in [-2, 2], \quad \text{OUTPUT} \in [-8.4, 9.3]
\end{array}
\right\}$$

### Level 4: Unit Conversion & Population Statistics
For the subset where $\text{UNIT} = \text{'K'}$:
$$T_{C, i} = T_{K, i} - 273.15$$
Population mean and standard deviation ($ddof = 0$):
$$\mu_C = \frac{1}{M}\sum_{i=1}^M T_{C, i}, \quad \sigma_C = \sqrt{\frac{1}{M}\sum_{i=1}^M (T_{C, i} - \mu_C)^2}$$

---

## 3. Directory Layout

```
01-practice-spy-mission/
├── docs/                      # Official challenge statements (PDF)
│   ├── level_1.pdf
│   ├── level_2.pdf
│   ├── level_3.pdf
│   └── level_4.pdf
├── data/                      # CSV datasets and competition archives
│   ├── data.csv
│   ├── train_data.csv
│   ├── test_data.csv
│   └── archives/
│       ├── input.zip
│       └── encrypted.zip      # Unlocked with password: metapoint
├── figures/                   # Generated figures
│   └── pca_metapoint_scatter.png
└── src/                       # Modular Python scripts
    ├── lvl1.py                # PCA standard deviation calculation
    ├── lvl2.py                # 2D projection and non-blocking figure export
    ├── lvl3.py                # NaN removal and outlier filtering
    └── lvl4.py                # Kelvin -> Celsius conversion and statistics
```

---

## 4. Execution Commands

From the project root or the `src/` directory:

```bash
# Level 1: Principal component computation
python 01-practice-spy-mission/src/lvl1.py

# Level 2: Generate 2D projection scatter plot
python 01-practice-spy-mission/src/lvl2.py

# Level 3: Clean data and count valid sample size
python 01-practice-spy-mission/src/lvl3.py

# Level 4: Kelvin -> Celsius conversion and statistical estimation
python 01-practice-spy-mission/src/lvl4.py
```
