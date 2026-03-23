import pandas as pd

# This script is to take out blank rows in the Lake_WSE column AND the rows in River_Node_WSE that have -1.00e+12.

# Load the reshaped CSV
input_csv = r"path\to\input.csv"
df = pd.read_csv(input_csv)

# Remove rows where Lake_WSE is NaN (missing) or River_Node_WSE is -1.00e+12 (invalid/missing)
df_cleaned = df.dropna(subset=["Lake_WSE"])
df_cleaned = df_cleaned[df_cleaned["River_Node_WSE"] != -1.00e+12]

# Save the cleaned data to a new CSV
output_csv = r"path\to\output.csv"
df_cleaned.to_csv(output_csv, index=False)

print(f"Cleaned data has been saved to {output_csv}")
