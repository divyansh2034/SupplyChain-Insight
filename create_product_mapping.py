import pandas as pd
import json

# Step 1: Load the original dataset
# Replace 'path/to/your/original_dataset.csv' with the actual path to your original dataset
original_df = pd.read_csv(r'C:\Users\div20\OneDrive\Desktop\supply-chain-blockchain\DataCoSupplyChainDataset.csv',encoding='latin1')

# Step 2: Load the processed dataset
# Replace 'path/to/your/processed_dataset.csv' with the actual path to your processed dataset
processed_df = pd.read_csv(r'C:\Users\div20\OneDrive\Desktop\supply-chain-blockchain\ProcessedDataCoSupplyChainDataset.csv',encoding='latin1')
sliced_processed_df = processed_df.iloc[:150000]
# Step 3: Create the mapping from numerical labels to product names
# Assuming the processed dataset has a column 'Label' for numerical labels
# and the original dataset has a column 'Product Name'
# Create a mapping from labels to product names based on the original dataset
product_mapping = {}

# Iterate through the processed dataset to create the mapping
for index, row in sliced_processed_df.iterrows():
    label = row['Product Name']  # Adjust this to the actual column name in your processed dataset
    product_name = original_df.loc[index, 'Product Name']  # Adjust this to the actual column name in your original dataset
    product_mapping[label] = product_name

# Print the mapping to verify
print("Product Mapping:")
for label, product in product_mapping.items():
    print(f"{label}: {product}")

# Step 4: Optionally, save the mapping to a file (e.g., JSON)
with open('product_mapping.json', 'w') as f:
    json.dump(product_mapping, f)

print("Product mapping saved to 'product_mapping.json'.")
