# swot-hydrology-analysis

This project analyzes the relationship between water surface elevation (WSE) from SWOT Level 2 Lake and River vector products (May–September 2024) using a Python-based geospatial data processing workflow.

## Project Overview

The goal of this project was to assess how well river WSE values explain lake WSE variability across the Mackenzie Delta Region. This was achieved by integrating, cleaning, and analyzing geospatial datasets using ArcGIS Pro and Python.

- `1_extract_wse.py` – Extract and aggregate WSE values from spatial datasets  
- `2_reshape_data.py` – Reshape dataset for analysis  
- `3_remove_nulls.py` – Clean dataset and remove invalid values  
- `4_ols_regression.py` – Perform regression analysis
  
## Workflow

### 1. Data Extraction (`1_extract_wse.py`)
- Intersected SWOT lake shapefiles with HydroLakes polygons using `arcpy.analysis.Intersect`
- Aggregated lake WSE values by HydroLake ID using the `Dissolve` tool
- Performed spatial joins between River Node shapefiles and HydroLakes using `arcpy.analysis.SpatialJoin`
- Extracted and combined lake and river WSE values into a single dataset
- Output: `wse_results_combined.csv`

### 2. Data Reshaping (`2_reshape_data.py`)
- Converted the dataset from wide format to long format using pandas
- Structured the data to align lake and river WSE values by date
- Output: reshaped CSV file

### 3. Data Cleaning (`3_remove_nulls.py`)
- Removed rows with missing lake WSE values
- Filtered out invalid river WSE values (e.g., -1.00e+12, representing missing or erroneous data)
- Output: cleaned dataset ready for analysis

### 4. Statistical Analysis (`4_ols_regression.py`)
- Grouped data by lake (HydroLake ID)
- Performed Ordinary Least Squares (OLS) regression using `statsmodels`
- Used River Node WSE as the independent variable and Lake WSE as the dependent variable
- Calculated R² values for lakes with sufficient observations (>5 records)
- Output: regression results per lake

## Tools & Technologies

- Python (arcpy, pandas, numpy, statsmodels)
- ArcGIS Pro
- Excel

## Note

The R² value represents the proportion of variance in lake WSE that can be explained by river WSE. Higher R² values indicate stronger relationships between lake and river dynamics.


- Data files are not included due to size and/or licensing constraints
- File paths in scripts must be updated
- Intermediate steps (e.g., adding dates to the top row in excel before script 2) were performed in Excel as part of preprocessing
