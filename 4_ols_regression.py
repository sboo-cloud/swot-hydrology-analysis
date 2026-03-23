import pandas as pd
import statsmodels.api as sm
import numpy as np

# 1: Input data
data = pd.read_csv(r"path\to\input.csv")

# 2: Create a list to store results for each lake
results = []

# 3: Group the data by Hylak_id (each lake)
grouped = data.groupby('Hylak_id')

# 4: Loop over each lake and perform OLS regression
for lake_id, group in grouped:
    if len(group) > 5:  # Only perform OLS if the lake has more than five entries

        X = group['River_Node_WSE']  # Explanatory variable (Independent)
        y = group['Lake_WSE']  # Dependent variable

        # Add a constant (intercept) to the explanatory variables
        X = sm.add_constant(X)

        # Perform OLS regression
        model = sm.OLS(y, X).fit()

        # Step 5: Extract the regression results (R-squared, coefficients)
        results.append({
            'Hylak_id': lake_id,
            'R_squared': model.rsquared,
            'Intercept': model.params[0],
            'Slope': model.params[1]
        })
    else:
        # If there's only one entry for the lake, store NaN for regression results
        results.append({
            'Hylak_id': lake_id,
            'R_squared': np.nan,
            'Intercept': np.nan,
            'Slope': np.nan
        })

# 6: Convert the results into a DataFrame
results_df = pd.DataFrame(results)

# 7: Save the results into a CSV file
results_df.to_csv(r"path\to\output.csv", index=False)


