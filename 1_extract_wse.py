import os
import csv
import arcpy

# This script is to get Lake WSE values and River Node wse values for the selected HydroLakes.
# Replace with your local file path

# Input path HydroLakes
hydrolakes_shapefile = r"path\to\input.shp"

# Where SWOT and River Nodes folders are stored
base_folder = r"path\to\input folder"

# Subfolder names (SWOT and River Node folders)
swot_folders = [
    "SWOT 468",
    "SWOT 496",
]

river_node_folders = [
    "River Node 496",
    "River Nodes 468"
]

# Create list of shapefiles
swot_shapefiles = []
river_node_shapefiles = []

# Loop through each SWOT folder to get shapefiles
for swot_folder in swot_folders:
    swot_folder_path = os.path.join(base_folder, swot_folder)
    if os.path.exists(swot_folder_path):
        for root, dirs, files in os.walk(swot_folder_path):
            for file in files:
                if file.endswith(".shp"):
                    swot_shapefiles.append(os.path.join(root, file))

# Loop through each River Node folder to get shapefiles
for river_node_folder in river_node_folders:
    river_node_folder_path = os.path.join(base_folder, river_node_folder)
    if os.path.exists(river_node_folder_path):
        for root, dirs, files in os.walk(river_node_folder_path):
            for file in files:
                if file.endswith(".shp"):
                    river_node_shapefiles.append(os.path.join(root, file))

# Output path
output_dir = r"path\to\output folder"
results = {}

# Process SWOT shapefiles
for swot_shapefile in swot_shapefiles:

    # Use the shapefile name for the column header
    shapefile_name = os.path.basename(swot_shapefile)

    # 1: Get lakes that intersect with HydroLakes
    intersected_lakes = os.path.join(output_dir, f"intersected_{shapefile_name}")
    arcpy.analysis.Intersect([swot_shapefile, hydrolakes_shapefile], intersected_lakes)

    # 2: Use Dissolve to aggregate the results
    dissolved_lakes = os.path.join(output_dir, f"dissolved_{shapefile_name}")
    arcpy.management.Dissolve(intersected_lakes, dissolved_lakes, ["Hylak_id"], statistics_fields=[["wse", "MEAN"]])

    # 3: Get data (Mean WSE, Hylak_id) from dissolved shapefile
    try:
        with arcpy.da.SearchCursor(dissolved_lakes, ['Hylak_id', 'MEAN_wse']) as cursor:
            for row in cursor:
                hylak_id = row[0]
                mean_wse = row[1]

                # Track the data for each Hylak_id
                if hylak_id not in results:
                    results[hylak_id] = {
                        'Hylak_id': hylak_id
                    }

                # Add the mean WSE for the current shapefile (SWOT data)
                results[hylak_id][shapefile_name] = mean_wse
    except Exception as e:
        print(f"Error during SearchCursor: {e}")

# Process River Node shapefiles
for river_node_shapefile in river_node_shapefiles:

    # Use shapefile name for the column header
    shapefile_name = os.path.basename(river_node_shapefile)

    # 1: Spatial Join with HydroLakes
    joined_rivernodes = os.path.join(output_dir, f"joined_{shapefile_name}")
    arcpy.analysis.SpatialJoin(hydrolakes_shapefile, river_node_shapefile, joined_rivernodes,
                               join_type="KEEP_COMMON", match_option="CLOSEST")

    # 2: Get data (WSE, Hylak_id) from the joined River Node shapefile
    try:
        with arcpy.da.SearchCursor(joined_rivernodes, ['Hylak_id', 'WSE']) as cursor:
            for row in cursor:
                hylak_id = row[0]
                wse_value = row[1]

                # Track the data for each Hylak_id
                if hylak_id not in results:
                    results[hylak_id] = {
                        'Hylak_id': hylak_id
                    }

                # Add the WSE for the River Node shapefile (for each date)
                results[hylak_id][shapefile_name] = wse_value
    except Exception as e:
        print(f"Error for River Node: {e}")

# Results to a CSV file
output_csv = os.path.join(output_dir, "wse_results_combined.csv")
try:
    with open(output_csv, 'w', newline='') as csvfile:

        # Write the fieldnames (columns)
        fieldnames = ['Hylak_id'] + [os.path.basename(shapefile) for shapefile in swot_shapefiles +
                                     river_node_shapefiles]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Write the data for each Hylak_id
        for hylak_id, data in results.items():
            writer.writerow(data)

    print(f"Results have been saved to {output_csv}")
except Exception as e:
    print(f"Error writing to CSV: {e}")