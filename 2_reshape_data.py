import pandas as pd

# This script is for reshaping the results from objective4.py because the results were formatted "wide" instead of
# "long".

# Load the edited CSV result file from 1_extract_wse.py that has the dates identified*
# *dates identified = open final csv file from 1_extract_wse.py and add dates to a top row
# then use that file as input for this


input_csv = r"path\to\input.csv"
df = pd.read_csv(input_csv)

# Strip any extra spaces in column names
df.columns = df.columns.str.strip()

# Rename 'Unnamed: 0' to 'Hylak_id'
df.rename(columns={'Unnamed: 0': 'Hylak_id'}, inplace=True)

# Check column names
print(df.columns)

# List to store reshaped data
reshaped_data = []

# Iterate through each row in the original DataFrame
for _, row in df.iterrows():
    hylak_id = row['Hylak_id']  # Extract Hylak_id

    # Iterate over each date column
    for date_column in df.columns[1:]:  # Skip the Hylak_id column
        if '.1' in date_column:

            # River Node WSE column
            lake_column = date_column.replace('.1', '')  # Remove .1 to get corresponding lake column

            # If the lake column exists in the DataFrame, extract its value
            if lake_column in df.columns:
                lake_wse = row[lake_column]
            else:
                lake_wse = None  # If there's no lake column, set as None

            # Extract the river node WSE from the ".1" column
            river_node_wse = row[date_column]

            # Add the reshaped data for lake WSE and river node WSE
            reshaped_data.append([hylak_id, date_column, lake_wse, river_node_wse])

# Convert reshaped data to a DataFrame
reshaped_df = pd.DataFrame(reshaped_data, columns=["Hylak_id", "Date", "Lake_WSE", "River_Node_WSE"])

# Save the reshaped data to a new CSV
output_csv = r"path\to\output.csv"
reshaped_df.to_csv(output_csv, index=False)

print(f"Reshaped data has been saved to {output_csv}")
