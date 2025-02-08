import pandas as pd
import numpy as np
import gc
import os
import warnings
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

warnings.filterwarnings('ignore')


class SupplyChainDataProcessor:
    def __init__(self, input_path, output_path, chunk_size=1000, max_rows=150000):
        self.input_path = input_path
        self.output_path = output_path
        self.chunk_size = chunk_size
        self.max_rows = max_rows
        
        # Read the exact column names from the CSV file
        print("Reading CSV headers...")
        sample_df = pd.read_csv(input_path, nrows=1, encoding='latin1')
        self.actual_columns = sample_df.columns.tolist()
        print("Actual columns in file:", self.actual_columns)
        
        # Create a mapping of lowercase to actual column names
        self.column_mapping = {col.lower(): col for col in self.actual_columns}
        
        # Define columns to keep with exact names from CSV
        self.columns_to_keep = [
            'Days for shipping (real)',
            'Days for shipment (scheduled)',
            'Benefit per order',
            'Sales per customer',
            'Delivery Status',
            'Late_delivery_risk',
            'Latitude',
            'Longitude',
            'Order City',
            'order date (DateOrders)',
            'Order Item Discount Rate',
            'Sales',
            'Order Item Total',
            'Order Profit Per Order',
            'Order Status',
            'Product Name',
            'Product Status',
            'shipping date (DateOrders)',
            'Product Price'
        ]
        
        self.columns_to_encode = [
            'Product Name',
            'Order City',
            'Delivery Status',
            'Order Status'
        ]
        
        self.date_columns = {
            'order date (DateOrders)': 'order_date',
            'shipping date (DateOrders)': 'shipping_date'
        }
        
        # Initialize label encoders
        self.label_encoders = {col: LabelEncoder() for col in self.columns_to_encode}
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    def process_dates(self, df):
        """Convert date columns to Unix timestamps"""
        for original_col, new_col in self.date_columns.items():
            if original_col in df.columns:
                try:
                    # Convert to datetime and then to Unix timestamp
                    df[new_col] = pd.to_datetime(df[original_col]).astype(np.int64) // 10**9
                    # Drop original date column
                    df = df.drop(columns=[original_col])
                except Exception as e:
                    print(f"Error processing date column {original_col}: {str(e)}")
                    # If date processing fails, drop the column
                    df = df.drop(columns=[original_col])
                    df[new_col] = np.nan
        
        return df

    def process_chunk(self, chunk):
        try:
            # Create a copy of the chunk to avoid warnings
            processed_chunk = chunk.copy()
            
            # Keep only the columns we want
            available_columns = [col for col in self.columns_to_keep if col in chunk.columns]
            processed_chunk = processed_chunk[available_columns]
            
            # Process date columns first
            processed_chunk = self.process_dates(processed_chunk)
            
            # Encode the specified columns
            for col in self.columns_to_encode:
                if col in processed_chunk.columns:
                    # Handle missing values
                    processed_chunk[col] = processed_chunk[col].fillna('Unknown')
                    # Encode the column
                    processed_chunk[col] = self.label_encoders[col].fit_transform(
                        processed_chunk[col].astype(str)
                    )
            
            # Print column names and a sample row for debugging
            if len(processed_chunk) > 0:
                print(f"\nColumns in processed chunk: {processed_chunk.columns.tolist()}")
                print(f"Sample row:\n{processed_chunk.iloc[0]}")
            
            return processed_chunk

        except Exception as e:
            print(f"Error processing chunk: {str(e)}")
            print(f"Available columns in chunk: {chunk.columns.tolist()}")
            return None

    def process_data(self):
        print("\nStarting data processing...")
        all_chunks = []

        try:
            # Read and process the CSV file in chunks
            for i, chunk in enumerate(pd.read_csv(self.input_path, 
                                                chunksize=self.chunk_size,
                                                nrows=self.max_rows,
                                                encoding='latin1')):
                print(f"\nProcessing chunk {i+1}...")
                processed_chunk = self.process_chunk(chunk)
                if processed_chunk is not None and not processed_chunk.empty:
                    all_chunks.append(processed_chunk)
                    print(f"Processed chunk {i+1} with {len(processed_chunk)} rows")

            if all_chunks:
                # Combine all processed chunks
                final_df = pd.concat(all_chunks, ignore_index=True)
                
                # Print information about the final DataFrame
                print("\nFinal DataFrame Info:")
                print(final_df.info())
                print("\nFinal columns:", final_df.columns.tolist())
                
                # Save to CSV
                final_df.to_csv(self.output_path, index=False)
                print(f"\nProcessing completed. Output saved to: {self.output_path}")
                print(f"Total rows processed: {len(final_df)}")
                
                # Verify the output
                print("\nVerifying output file...")
                output_df = pd.read_csv(self.output_path, nrows=5)
                print("Columns in output file:", output_df.columns.tolist())
            else:
                print("No data was processed. Please check the input file and columns.")

        except Exception as e:
            print(f"Error during processing: {str(e)}")


# Usage example
if __name__ == "__main__":
    input_file = r"C:\Users\div20\OneDrive\Desktop\supply-chain-blockchain\DataCoSupplyChainDataset.csv"
    output_file = r"C:\Users\div20\OneDrive\Desktop\supply-chain-blockchain\ProcessedDataCoSupplyChainDataset.csv"

    processor = SupplyChainDataProcessor(
        input_path=input_file,
        output_path=output_file,
        chunk_size=1000,
        max_rows=150000
    )

    processor.process_data()
