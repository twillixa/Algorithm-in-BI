import pandas as pd

# Load the two CSV files
clients_file = "export clients R7AL 11.03.2026.csv"
orders_file = "export comandes R7AL 11.03.2026.csv"

# You might need to adjust the delimiter or encoding if there are read errors
clients_df = pd.read_csv(clients_file)
orders_df = pd.read_csv(orders_file)

# Standardize the 'Email' column name before joining
# Clients file has 'EMAIL', Orders file has 'Email'
if 'Email' in orders_df.columns and 'EMAIL' not in orders_df.columns:
    orders_df.rename(columns={'Email': 'EMAIL'}, inplace=True)

# Convert emails to lowercase to ensure matching works properly
clients_df['EMAIL'] = clients_df['EMAIL'].str.lower().str.strip()
orders_df['EMAIL'] = orders_df['EMAIL'].str.lower().str.strip()

# Perform the join on the 'EMAIL' column
# You can change how='inner' to 'left', 'right', or 'outer' depending on what results you want
merged_df = pd.merge(clients_df, orders_df, on='EMAIL', how='inner')

# Export the merged dataframe to a new CSV file
output_file = "merged_clients_orders.csv"
merged_df.to_csv(output_file, index=False)

print(f"Join completed! The result has been saved to: {output_file}")
print(f"Number of matched rows: {len(merged_df)}")
