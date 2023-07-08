import os
import pandas as pd

#1. Combinining whole month data:
# Set the path to the folder containing the Excel files
path = './aws_logs/'

# Get a list of all Excel files in the folder
files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.xlsx')]

# Initialize an empty list to store the dataframes
df_list = []

# Loop through the Excel files and combine the dataframes
for file in files:
    # Read each sheet in the Excel file and add a date column
    sheets = pd.read_excel(file, sheet_name=None)
    for name, sheet in sheets.items():
        sheet.insert(0,'Date', os.path.splitext(os.path.basename(file))[0])
        df_list.append(sheet)
    print('Loading file {0}...'.format(file))

# Concatenate the dataframes into a single dataframe
combined_df = pd.concat(df_list, axis=0)

# Write the combined dataframe to a new Excel file
writer = pd.ExcelWriter('combined_data.xlsx', engine='xlsxwriter')
combined_df.to_excel(writer, index=False)
writer.save()
# ==================================================================================
#2. Transforming into Pivot Table

# Load the Excel file
file_path = './combined_data.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Create a pivot table from the data
pivot_table = pd.pivot_table(df, index='Date', columns='clientId', values='count()', aggfunc='sum')

# Output the pivot table to Sheet2 in the same file
with pd.ExcelWriter(file_path, mode='w') as writer:
    pivot_table.to_excel(writer, sheet_name='logs')
