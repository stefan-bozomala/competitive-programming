# Cloudflight Coding Contest (CCC) – 41st Edition: Data & AI Track
### *Methodological Frameworks, Deep Neural Regression, and Latent Space Steganographic Analysis in High-Dimensional Manifolds*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red.svg)](https://pytorch.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15%2B-FF6F00.svg)](https://www.tensorflow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Contest](https://img.shields.io/badge/Cloudflight_CCC-41st_Data%2FAI-purple.svg)](https://cloudflight.io/)

---

## Author & Academic Affiliation

- **Author / Researcher:** **Ștefan Bozomala**
- **Academic Affiliation:** Technical University of Cluj-Napoca (UTCN), Romania
- **GitHub:** [@BozomalaStefan-30126](https://github.com/BozomalaStefan-30126)
- **Institutional Email:** `Bozomala.So.Stefan@student.utcluj.ro`
- **Competition Event:** 41st Cloudflight Coding Contest (Data & AI Track)
- **Date:** November 14, 2025
- **Official Venue:** CREIC – Regional Centre of Excellence for Creative Industries, Cluj-Napoca, Romania
- **Organizer:** Cloudflight GmbH (Munich, Germany)
- **Official Participation Certificate:** Documented in [`docs/ccc-participation-certificate-41st-data-ai-ccc-2025-5774.pdf`](docs/ccc-participation-certificate-41st-data-ai-ccc-2025-5774.pdf) (ID: `#5774`).

---

## Abstract

This repository provides the complete algorithmic pipelines, mathematical formulations, predictive architectures, and empirical findings developed for the **41st Cloudflight Coding Contest (Data & AI Discipline)**. The project addresses two challenging paradigms in applied data science and artificial intelligence:

1. **Practice Track (*AI: Spy Mission*):** A cyber-forensics analytical challenge formulated around unsupervised feature extraction and data cleansing. By projecting high-dimensional transducer data onto a 2D latent manifold using **Principal Component Analysis (PCA)**, we demonstrate the steganographic recovery of a cryptographic access key (`metapoint`). Subsequently, missing value handling, physical domain boundary-based anomaly detection, and thermodynamic unit standardization ($K \to ^\circ\text{C}$) are applied to prepare clean training data.
2. **Official Live Competition (*Ecological Habitability Modeling – Bird Love Score*):** Multi-variable predictive modeling of an ecological compatibility metric for *Birds of Paradise* (BOP) habitats. The methodology integrates lexical numeral parsing, multi-tier composite sorting across microclimatic attributes, heuristic thermodynamic unit disambiguation ($^\circ\text{F} \to ^\circ\text{C}$), multi-source tabular data fusion, and the training of a **Deep Artificial Neural Network (Deep MLP)** regression architecture with LeakyReLU activations and Adam optimization.

---

## Repository Architecture

The codebase is structured hierarchically to maintain clean separation between raw datasets, problem statements, generated outputs, and modular source code:

```text
cloudflight-coding-contest-41/
├── .gitignore                          # Comprehensive exclusions (bytecode, .venv, IDEs, OS metadata)
├── LICENSE                             # MIT Open-Source License
├── README.md                           # Master Academic Documentation
├── requirements.txt                    # Python dependencies for Scientific Computing & ML
├── docs/                               # Official certificates and empirical proof assets
│   ├── ccc-participation-certificate-41st-data-ai-ccc-2025-5774.pdf  # Verified CCC #5774 Certificate
│   └── assets/
│       └── 20251113_200006.jpg         # Competition photo (latent PCA scatter plot on screen)
├── 01-practice-spy-mission/            # Module 1: Practice Track "AI: Spy Mission"
│   ├── README.md                       # Dedicated module documentation
│   ├── docs/                           # Official problem statements (PDF)
│   │   ├── level_1.pdf                 # Level 1: Dimensionality reduction (PCA)
│   │   ├── level_2.pdf                 # Level 2: 2D scatter plot & password extraction
│   │   ├── level_3.pdf                 # Level 3: Missing value handling & outlier filtering
│   │   └── level_4.pdf                 # Level 4: Thermodynamic unit standardization
│   ├── data/                           # Tabular datasets & contest archives
│   │   ├── data.csv                    # Transducer dataset for PCA
│   │   ├── train_data.csv              # Noisy sensor training data with outliers
│   │   ├── test_data.csv               # Test set for downstream evaluation
│   │   └── archives/
│   │       ├── input.zip               # Original USB drive bundle
│   │       └── encrypted.zip           # Encrypted archive (password: metapoint)
│   ├── figures/                        # Generated visual artifacts
│   │   └── pca_metapoint_scatter.png   # 2D projection revealing the word "metapoint"
│   └── src/                            # Modular Python solutions (dynamic path resolution)
│       ├── lvl1.py                     # PCA & standard deviation computation
│       ├── lvl2.py                     # 2D projection & automated plot generation
│       ├── lvl3.py                     # NaN filtering & physical boundary outlier rejection
│       └── lvl4.py                     # Kelvin -> Celsius conversion & statistical estimators
└── 02-competition-41st-ccc/            # Module 2: Official Live Competition (CREIC Cluj-Napoca)
    ├── README.md                       # Dedicated module documentation
    ├── data/
    │   ├── level_1/                    # Level 1 input files (.in) & official samples (.out)
    │   │   ├── level_1_sample.in / .out
    │   │   ├── level_1_a.in
    │   │   ├── level_1_b.in
    │   │   ├── level_1_c.in
    │   │   ├── level_1_d.in
    │   │   └── level_1_e.in
    │   ├── level_2/                    # Level 2 input files (.in) & aggregated historical data
    │   │   ├── level_2_sample.in / .out
    │   │   ├── level_2_a.in
    │   │   ├── level_2_b.in
    │   │   ├── level_2_c.in
    │   │   └── all_data_from_level_1.in
    │   ├── archives/                   # Official challenge ZIP packages
    │   │   ├── level_1.zip
    │   │   └── level_2.zip
    │   └── results/                    # Validated solutions generated by the pipeline
    │       ├── level_1_sample.txt, level_1_a.txt ... level_1_e.txt
    │       ├── level_1_c.txt           # Ordered BOP identifier sequence
    │       ├── raspuns_b.csv           # Model inference output (Set B - 200 records)
    │       └── raspuns_c.csv           # Model inference output (Set C - 100 records)
    └── src/
        ├── NIVEL1.py                   # Multi-attribute sorting & lexical numeral parser
        └── varianta_finala_de_cod.py   # Full pipeline (Level 1 + Deep ANN Regression Level 2)
```

---

## Theoretical Foundations & Mathematical Formulations

### 1. Principal Component Analysis (PCA) & Latent Space Steganography

Let $X \in \mathbb{R}^{N \times D}$ denote the matrix of raw observations, where $N$ is the number of sensor samples and $D$ represents the initial feature dimensionality.

#### Standardization
To prevent features with larger variance from dominating the spectral decomposition, columns are standardized to zero mean and unit variance:
$$Z_{i, j} = \frac{X_{i, j} - \mu_j}{\sigma_j}, \quad \mu_j = \frac{1}{N}\sum_{i=1}^N X_{i,j}, \quad \sigma_j = \sqrt{\frac{1}{N}\sum_{i=1}^N (X_{i,j} - \mu_j)^2}$$

#### Empirical Covariance and Spectral Decomposition
The empirical covariance matrix $\Sigma \in \mathbb{R}^{D \times D}$ is defined as:
$$\Sigma = \frac{1}{N - 1} Z^T Z$$
Through eigendecomposition (or Singular Value Decomposition $Z = U S V^T$):
$$\Sigma v_k = \lambda_k v_k, \quad k \in \{1, \dots, D\}$$
where $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_D \ge 0$ denote the eigenvalues (explained variance) associated with eigenvectors $v_k \in \mathbb{R}^D$. The standard deviation along each principal axis is given by:
$$\sigma_k = \sqrt{\lambda_k} = \frac{S_k}{\sqrt{N - 1}}$$

#### Latent Manifold Projection & Steganographic Key Recovery
Dimensionality reduction onto the leading $k=2$ components is performed via projection matrix $W_2 = [v_1, v_2] \in \mathbb{R}^{D \times 2}$:
$$Z_{2D} = Z W_2$$
Due to the latent geometric distribution of data points, applying a vertical parity reflection:
$$\begin{pmatrix} x' \\ y' \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix}$$
recovers the Latin characters: **`metapoint`**, representing the secret password required to decrypt `encrypted.zip`.

---

### 2. Multi-Attribute Data Cleansing & Thermodynamic Disambiguation

Sensor acquisition errors introduce missing values (`NaN`) and anomalous physical outliers. The valid observation space $\mathcal{X}_{\text{valid}}$ is formally bounded by the physical sensor domains:

$$\mathcal{X}_{\text{valid}} = \left\{ \mathbf{x} \in \mathbb{R}^6 \ \middle|\ 
\begin{aligned}
\text{AMPS} &\in [0.00, 1.00] \\
\text{VOLTS} &\in [0.02, 8.70] \\
\text{TEMP} &\in [-100.00, 373.15] \\
\text{DELTA} &\in [-1.00, 1.00] \\
\text{GAMMA} &\in [-2.00, 2.00] \\
\text{OUTPUT} &\in [-8.40, 9.30]
\end{aligned}
\right\} \setminus \{ \mathbf{x} \mid \exists j, x_j = \text{NaN} \}$$

#### Thermodynamic Unit Conversion
In the cleaned dataset, temperatures are measured across mixed thermometric scales (Kelvin, Celsius, Fahrenheit):
- For records with $\text{UNIT} = \text{'K'}$:
  $$T_{C} = T_{K} - 273.15$$
  Population statistical estimators ($ddof = 0$):
  $$\mu_C = \frac{1}{M}\sum_{i=1}^M T_{C, i} = -0.69^\circ\text{C}, \quad \sigma_C = \sqrt{\frac{1}{M}\sum_{i=1}^M (T_{C, i} - \mu_C)^2} = 48^\circ\text{C}$$
- In ecological modeling where temperatures exceed $60^\circ$ (indicating accidental recording in Fahrenheit):
  $$T_{C} = \frac{5}{9}(T_{F} - 32)$$

---

### 3. Deep Neural Network (ANN) Regression for Ecological Compatibility

To model the nonlinear mapping from environmental indicators to the continuous target $y = \text{Bird Love Score [<3]}$, a deep Multilayer Perceptron (MLP) architecture was implemented.

#### Network Topology
The model takes a 5-dimensional standardized input vector:
$$\mathbf{x} = \begin{bmatrix} \text{BOP}, & \text{Vegetation [\%]}, & \text{Insects [g/m²]}, & \text{Urban Light [\%]}, & T_C, & \text{Humidity [\%]} \end{bmatrix}^T$$

The forward computation through 7 dense layers is defined by:
$$\mathbf{h}_1 = \phi(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1), \quad \mathbf{W}_1 \in \mathbb{R}^{128 \times 5}$$
$$\mathbf{h}_2 = \phi(\mathbf{W}_2 \mathbf{h}_1 + \mathbf{b}_2), \quad \mathbf{W}_2 \in \mathbb{R}^{64 \times 128}$$
$$\mathbf{h}_3 = \phi(\mathbf{W}_3 \mathbf{h}_2 + \mathbf{b}_3), \quad \mathbf{W}_3 \in \mathbb{R}^{64 \times 64}$$
$$\mathbf{h}_4 = \phi(\mathbf{W}_4 \mathbf{h}_3 + \mathbf{b}_4), \quad \mathbf{W}_4 \in \mathbb{R}^{32 \times 64}$$
$$\mathbf{h}_5 = \phi(\mathbf{W}_5 \mathbf{h}_4 + \mathbf{b}_5), \quad \mathbf{W}_5 \in \mathbb{R}^{16 \times 32}$$
$$\mathbf{h}_6 = \phi(\mathbf{W}_6 \mathbf{h}_5 + \mathbf{b}_6), \quad \mathbf{W}_6 \in \mathbb{R}^{4 \times 16}$$
$$\hat{y} = \mathbf{W}_7 \mathbf{h}_6 + b_7, \quad \mathbf{W}_7 \in \mathbb{R}^{1 \times 4}$$

#### LeakyReLU Activation Function
To mitigate gradient vanishing and prevent dying neurons during deep backpropagation, LeakyReLU is utilized with negative slope $\alpha = 0.01$:
$$\phi(z) = \max(\alpha z, z) = \begin{cases} z, & z > 0 \\ 0.01 z, & z \le 0 \end{cases}$$

#### Optimization Objective
- **Loss Function:** Mean Squared Error (MSE):
  $$\mathcal{L}_{\text{MSE}}(\theta) = \frac{1}{N}\sum_{i=1}^N \left( y_i - \hat{y}_i \right)^2$$
- **Evaluation Metric:** Root Mean Squared Error (RMSE):
  $$\text{RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^N \left( y_i - \hat{y}_i \right)^2}$$
- **Optimizer:** Adam (Adaptive Moment Estimation) with first and second moment decay parameters $\beta_1 = 0.9, \beta_2 = 0.999$:
  $$m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t, \quad v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2$$
  $$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}, \quad \theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$

---

## Experimental Results & Benchmark Summary

### Track 1: Practice Challenge (AI: Spy Mission)

| Level | Technical Objective | Computed Value / Outcome | Ground Truth Validation |
|---|---|---|---|
| **Level 1** | Standard deviations of top 2 PCA components | $\sigma_1 = 1.97, \quad \sigma_2 = 1.00$ | Confirmed via SVD & covariance matrix |
| **Level 2** | Cryptographic key in latent scatter plot | `metapoint` | Successfully unlocks `encrypted.zip` |
| **Level 3** | Valid samples after NaN & outlier rejection | `971` rows (from 1000 initial) | `16 NaN`, `13 outliers` pruned |
| **Level 4** | Statistics of converted Kelvin temperatures | Mean: `-0.69` $^\circ\text{C}$, Std: `48` $^\circ\text{C}$ | `221` Kelvin records converted |

### Track 2: Official Live Competition (41st CCC)

| Level | Dataset | Records (BOP) | Methodology | Generated Output |
|---|---|---|---|---|
| **Level 1** | `level_1_sample.in` | 4 | Lexical normalization + Compound sort | `level_1_sample.txt` (Matches sample.out) |
| **Level 1** | `level_1_a.in` | 5 | Lexical normalization + Compound sort | `level_1_a.txt` |
| **Level 1** | `level_1_b.in` | 51 | Lexical normalization + Compound sort | `level_1_b.txt` |
| **Level 1** | `level_1_c.in` | 200 | Lexical normalization + Compound sort | `level_1_c.txt` (Validated) |
| **Level 1** | `level_1_d.in` | 73 | Lexical normalization + Compound sort | `level_1_d.txt` |
| **Level 1** | `level_1_e.in` | 2171 | Lexical normalization + Compound sort | `level_1_e.txt` |
| **Level 2** | `level_2_b.in` | 200 | Multi-source fusion + Deep ANN Regression | `raspuns_b.csv` (Validated) |
| **Level 2** | `level_2_c.in` | 100 | Multi-source fusion + Deep ANN Regression | `raspuns_c.csv` (Validated) |

---

## Installation & Reproducibility Guide

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/BozomalaStefan-30126/cloudflight-coding-contest-41.git
cd cloudflight-coding-contest-41

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux / macOS:
# source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### 2. Executing Practice Track Pipelines (Spy Mission)

```bash
# Level 1: Compute PCA explained variance and standard deviations
python 01-practice-spy-mission/src/lvl1.py

# Level 2: Generate 2D scatter plot and save figure to figures/
python 01-practice-spy-mission/src/lvl2.py

# Level 3: Clean NaN rows and filter sensor outliers
python 01-practice-spy-mission/src/lvl3.py

# Level 4: Perform thermodynamic conversion and compute population statistics
python 01-practice-spy-mission/src/lvl4.py
```

### 3. Executing Live Competition Solutions (41st CCC)

The pipeline automatically detects available runtimes and operates interchangeably on **TensorFlow/Keras** or **PyTorch**:

```bash
# Level 1: Process all input batches (sample, a, b, c, d, e)
python 02-competition-41st-ccc/src/NIVEL1.py

# Level 1 & 2: Complete end-to-end pipeline with Neural Network regression
python 02-competition-41st-ccc/src/varianta_finala_de_cod.py
```

---

## References & Citations

1. **Cloudflight Coding Contest (CCC):** [https://cloudflight.io/coding-contest/](https://cloudflight.io/coding-contest/)
2. **Official Contest Platform:** [https://codingcontest.org/](https://codingcontest.org/)
3. **CREIC – Regional Centre of Excellence for Creative Industries:** Cluj-Napoca, Romania.
4. **Scikit-Learn:** Pedregosa, F., et al., *Scikit-learn: Machine Learning in Python*, Journal of Machine Learning Research (JMLR), 12, pp. 2825–2830, 2011.
5. **Adam Optimizer:** Kingma, D. P., & Ba, J., *Adam: A Method for Stochastic Optimization*, International Conference on Learning Representations (ICLR), 2015.

---

## License

This project is released under the **MIT License**. Refer to [`LICENSE`](LICENSE) for full legal text.
