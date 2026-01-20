# TOPSIS Ranking System (Python Package + Web Service)

This repository implements **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)**, a widely used **Multi-Criteria Decision Making (MCDM)** method.  
The project contains:

✅ **Part-I:** Command-line TOPSIS program (`topsis.py`)  
✅ **Part-II:** Python package uploaded to PyPI (with CLI command `topsis`)  
✅ **Part-III:** Flask-based web service (file upload + TOPSIS result + download/email)

---

## Table of Contents
- [What is TOPSIS?](#what-is-topsis)
- [Methodology (Step-by-step)](#methodology-step-by-step)
- [Input Format](#input-format)
- [Output Format](#output-format)
- [How to Run](#how-to-run)
  - [Part-I: Command Line Program](#part-i-command-line-program)
  - [Part-II: Python Package](#part-ii-python-package)
  - [Part-III: Web Service](#part-iii-web-service)
- [Result Table Explanation](#result-table-explanation)
- [Project Structure](#project-structure)
- [Common Issues & Fixes](#common-issues--fixes)
- [License](#license)

---

## What is TOPSIS?
TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) is a ranking algorithm used when we have multiple alternatives and multiple criteria.  
The best alternative is the one that is:

✅ Closest to the **Ideal Best Solution**  
✅ Farthest from the **Ideal Worst Solution**

This is useful in:
- Product evaluation
- College selection
- Investment/portfolio selection
- Hiring decision scoring
- Supplier selection

---

## Methodology (Step-by-step)

Let us assume a dataset of **m alternatives** and **n criteria**:

| Alternative | C1 | C2 | ... | Cn |
|------------|----|----|-----|----|
| A1         | x11| x12| ... | x1n|
| A2         | x21| x22| ... | x2n|
| ...        | ...| ...| ... | ...|
| Am         | xm1| xm2| ... | xmn|

### ✅ Step 1: Normalize the Decision Matrix
We normalize each criterion using **vector normalization**:

\[
r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{i=1}^{m} x_{ij}^2}}
\]

This makes all criteria comparable even if they have different scales.

---

### ✅ Step 2: Apply Weights
Each criterion has a weight (importance). Weighted normalized matrix is:

\[
v_{ij} = r_{ij} \cdot w_j
\]

where \(w_j\) is the weight of criterion \(j\).

---

### ✅ Step 3: Determine Ideal Best and Ideal Worst
We create two hypothetical alternatives:

- **Ideal Best (A⁺)**: best values for each criterion  
- **Ideal Worst (A⁻)**: worst values for each criterion  

Impacts are used here:

- If impact is `+` (benefit): larger is better  
- If impact is `-` (cost): smaller is better  

\[
A^+ = \{v_1^+, v_2^+, ..., v_n^+\}
\]
\[
A^- = \{v_1^-, v_2^-, ..., v_n^-\}
\]

---

### ✅ Step 4: Calculate Euclidean Distance
Distance from ideal best:

\[
S_i^+ = \sqrt{\sum_{j=1}^{n}(v_{ij}-v_j^+)^2}
\]

Distance from ideal worst:

\[
S_i^- = \sqrt{\sum_{j=1}^{n}(v_{ij}-v_j^-)^2}
\]

---

### ✅ Step 5: Calculate TOPSIS Score
\[
C_i = \frac{S_i^-}{S_i^+ + S_i^-}
\]

Range:
- \(C_i \in [0,1]\)
- Higher score = better alternative

---

### ✅ Step 6: Rank Alternatives
Sort based on TOPSIS score in **descending order**.  
Highest TOPSIS score → **Rank 1**

---

## Input Format
The input file must be a `.csv` file with:

- 1st column: **Alternative name / ID**  
- 2nd onwards: **numeric criteria values**

✅ Example:

-csv
Fund Name,P1,P2,P3,P4
M1,0.67,0.45,6.5,12.56
M2,0.60,0.38,6.7,14.47
M3,0.82,0.67,3.8,17.10
M4,0.76,0.58,4.8,12.29

Output Format

The output CSV file contains all original columns + 2 extra columns:
-Topsis Score
-Rank
✅ Example:
| Fund Name | P1   | P2   | P3  | P4   | Topsis Score | Rank |
| --------- | ---- | ---- | --- | ---- | ------------ | ---- |
| M3        | 0.82 | 0.67 | 3.8 | 17.1 | 0.812345     | 1    |
| M4        | 0.76 | 0.58 | 4.8 | 12.3 | 0.704211     | 2    |
| ...       | ...  | ...  | ... | ...  | ...          | ...  |


## How to Run

# Part-I: Command Line Program
Go to Part-I folder:
cd Part-I
pip install numpy pandas
python topsis.py sample_input.csv "1,1,1,2" "+,+,-,+" output.csv

# Part-II: Python Package
Install package locally:
cd Part-II-PyPI-Package/Topsis-Harith-102303243
pip install .

Run CLI:
topsis sample_input.csv "1,1,1,2" "+,+,-,+" output.csv

# Part-III: Web Service
Install requirements:
cd Part-III-Web-Service
pip install -r requirements.txt
python app.py

Open: http://127.0.0.1:5000/
Upload file → enter weights/impacts → Run TOPSIS → Download result



## Result Table Explanation

The results table contains ranking information:
# TOPSIS Score
-Shows closeness to ideal solution
-Higher value indicates better alternative

# Rank
-Rank 1 is the best alternative
-Rank increases as score decreases

This provides a complete decision-making view with transparent scoring.



## Project Structure

TOPSIS_Full_Submission/
│
├── Part-I/
│   ├── topsis.py
│   └── sample_input.csv
│
├── Part-II-PyPI-Package/
│   └── Topsis-Harith-102303243/
│       ├── pyproject.toml
│       ├── README.md
│       ├── src/
│       └── tests/
│
└── Part-III-Web-Service/
    ├── app.py
    ├── requirements.txt
    └── templates/
        └── index.html



## Common Issues & Fixes

1. File Not Found
Ensure the CSV is in the same folder OR use full path.

2. Non-numeric data
Ensure columns from 2nd onwards contain numeric values only.

3. Weights/impacts mismatch
Number of weights and impacts must equal number of criteria.

Example:
Criteria = 4 columns → weights = 4 values, impacts = 4 symbols.



## License
This project is licensed under the MIT License.
