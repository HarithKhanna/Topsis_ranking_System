import sys
import os
import pandas as pd
import numpy as np


def error_exit(msg: str):
    print(f"Error: {msg}")
    sys.exit(1)


def parse_list(arg: str, name: str):
    if "," not in arg:
        error_exit(f"{name} must be separated by ',' (comma). Example: 1,1,2")
    parts = [x.strip() for x in arg.split(",") if x.strip() != ""]
    if len(parts) == 0:
        error_exit(f"{name} cannot be empty.")
    return parts


def validate_inputs(input_file, weights_str, impacts_str, output_file):
    if not os.path.exists(input_file):
        error_exit(f"File not found: {input_file}")

    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        error_exit(f"Unable to read input file. Ensure it's a valid CSV. Details: {e}")

    if df.shape[1] < 3:
        error_exit("Input file must contain three or more columns (1 name/id column + >=2 criteria columns).")

    criteria_cols = df.columns[1:]
    criteria = df[criteria_cols].copy()

    for col in criteria_cols:
        criteria[col] = pd.to_numeric(criteria[col], errors="coerce")

    if criteria.isna().any().any():
        bad_cols = criteria.columns[criteria.isna().any()].tolist()
        error_exit(f"Non-numeric value(s) found in criteria columns: {bad_cols}")

    weights = parse_list(weights_str, "Weights")
    impacts = parse_list(impacts_str, "Impacts")

    n_criteria = len(criteria_cols)
    if len(weights) != n_criteria:
        error_exit(f"Number of weights ({len(weights)}) must match number of criteria columns ({n_criteria}).")
    if len(impacts) != n_criteria:
        error_exit(f"Number of impacts ({len(impacts)}) must match number of criteria columns ({n_criteria}).")

    try:
        weights = [float(w) for w in weights]
    except:
        error_exit("Weights must be numeric values separated by commas. Example: 1,1,2")

    if any(w <= 0 for w in weights):
        error_exit("Weights must be positive numbers.")

    impacts = [imp.strip() for imp in impacts]
    for imp in impacts:
        if imp not in ["+", "-"]:
            error_exit("Impacts must be either '+' or '-' separated by commas. Example: +,+,-,+")

    return df, criteria_cols, np.array(weights, dtype=float), impacts


def topsis(df, criteria_cols, weights, impacts):
    X = df[criteria_cols].astype(float).values
    denom = np.sqrt((X ** 2).sum(axis=0))
    if np.any(denom == 0):
        error_exit("One or more criteria columns have all zero values, cannot normalize.")
    R = X / denom

    W = weights / weights.sum()
    V = R * W

    ideal_best = np.zeros(V.shape[1])
    ideal_worst = np.zeros(V.shape[1])

    for j in range(V.shape[1]):
        if impacts[j] == "+":
            ideal_best[j] = V[:, j].max()
            ideal_worst[j] = V[:, j].min()
        else:
            ideal_best[j] = V[:, j].min()
            ideal_worst[j] = V[:, j].max()

    S_plus = np.sqrt(((V - ideal_best) ** 2).sum(axis=1))
    S_minus = np.sqrt(((V - ideal_worst) ** 2).sum(axis=1))

    score = S_minus / (S_plus + S_minus)
    rank = score.argsort()[::-1].argsort() + 1

    return score, rank


def main():
    if len(sys.argv) != 5:
        print("Usage:")
        print("  python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>")
        print("Example:")
        print('  python topsis.py data.csv "1,1,1,2" "+,+,-,+" output-result.csv')
        sys.exit(1)

    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    output_file = sys.argv[4]

    df, criteria_cols, weights, impacts = validate_inputs(input_file, weights_str, impacts_str, output_file)
    score, rank = topsis(df, criteria_cols, weights, impacts)

    df["Topsis Score"] = np.round(score, 6)
    df["Rank"] = rank

    try:
        df.to_csv(output_file, index=False)
    except Exception as e:
        error_exit(f"Failed to write output file. Details: {e}")

    print(f"Success: TOPSIS result saved to '{output_file}'")


if __name__ == "__main__":
    main()
