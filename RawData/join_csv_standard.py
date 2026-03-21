import csv
import sys

clients_file = "export clients R7AL 11.03.2026.csv"
orders_file = "export comandes R7AL 11.03.2026.csv"
output_file = "merged_clients_orders.csv"

# 1. Read the clients file into a dictionary grouped by normalized email
# Some values might have different capitalizations, so we lowercase them
clients_dict = {}

try:
    with open(clients_file, 'r', encoding='latin-1') as f_clients:
        reader = csv.DictReader(f_clients)
        # Verify the EMAIL field exists
        if 'EMAIL' not in reader.fieldnames:
            print("Error: 'EMAIL' column not found in clients file.")
            sys.exit(1)
            
        client_fields = reader.fieldnames
        for row in reader:
            email = row.get('EMAIL', '').strip().lower()
            if email:
                clients_dict[email] = row
except Exception as e:
    print(f"Failed to read clients file: {e}")
    sys.exit(1)

# 2. Open orders file and prepare to write out the joined result
joined_rows = []
try:
    with open(orders_file, 'r', encoding='latin-1') as f_orders:
        reader = csv.DictReader(f_orders)
        
        # Determine the email column name in orders file
        order_email_col = 'Email'
        if 'Email' not in reader.fieldnames and 'EMAIL' in reader.fieldnames:
            order_email_col = 'EMAIL'
            
        order_fields = reader.fieldnames
        
        # The fields for our merged file will be all order fields + all client fields (without duplicating email)
        client_fields_to_add = [f for f in client_fields if f.lower() != 'email']
        output_fields = order_fields + client_fields_to_add
        
        with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=output_fields)
            writer.writeheader()
            
            matched_count = 0
            for row in reader:
                email = row.get(order_email_col, '').strip().lower()
                
                # If we find the email in the clients dict, we merge the row
                if email in clients_dict:
                    client_data = clients_dict[email]
                    merged_row = row.copy()
                    for f in client_fields_to_add:
                        merged_row[f] = client_data.get(f, '')
                    
                    writer.writerow(merged_row)
                    matched_count += 1
                    
            print(f"Join completed successfully using pure Python! The result has been saved to: {output_file}")
            print(f"Found {matched_count} matching orders based on the email address.")
except Exception as e:
    print(f"Failed to read orders or save joined file: {e}")
    sys.exit(1)
