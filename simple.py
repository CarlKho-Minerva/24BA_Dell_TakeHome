import pandas as pd
import csv
from typing import Tuple, List, Dict
import numpy as np
from tabulate import tabulate

def reconcile_transaction_records(file1_path: str, file2_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Efficiently reconcile transaction records between two CSV files.

    Time Complexity: O(n log n) due to merging and set operations
    Space Complexity: O(n) where n is the total number of transactions

    Args:
        file1_path (str): Path to the first CSV file (ServiceCodes_ECB)
        file2_path (str): Path to the second CSV file (ServiceCodes_TAR)

    Returns:
        Tuple of DataFrames containing discrepancies and missing transactions
    """
    # Optimized CSV reading with efficient parsing
    def read_csv_optimized(file_path: str) -> pd.DataFrame:
        """
        Read CSV with optimized parsing and minimal memory overhead.

        Args:
            file_path (str): Path to the CSV file

        Returns:
            DataFrame with cleaned and standardized data
        """
        # Use more memory-efficient reading
        df = pd.read_csv(
            file_path,
            low_memory=False,  # Avoid mixed-type inference warnings
            dtype={
                'SPA': 'category',  # Memory-efficient categorical type
                'Service Code': 'category',
                'Charge': 'float32',
                'Stop Date': 'object',  # Keep as string for exact matching
                'New Charge': 'float32'
            },
            na_filter=False  # Faster parsing by avoiding NaN detection
        )

        # Strip whitespace and normalize columns
        df.columns = [col.strip().title() for col in df.columns]
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.strip()

        return df

    # Read files efficiently
    df1 = read_csv_optimized(file1_path)
    df2 = read_csv_optimized(file2_path)

    # Create unique keys using vectorized operations
    df1['Unique_Key'] = df1['Spa'] + '_' + df1['Service_Code']
    df2['Unique_Key'] = df2['Spa'] + '_' + df2['Service_Code']

    # Identify missing transactions using set operations
    set1 = set(df1['Unique_Key'])
    set2 = set(df2['Unique_Key'])

    missing_in_file1 = df2[~df2['Unique_Key'].isin(set1)]
    missing_in_file2 = df1[~df1['Unique_Key'].isin(set2)]

    # Efficient discrepancy detection
    merged = pd.merge(df1, df2, on='Unique_Key', suffixes=('_ECB', '_TAR'))

    # Vectorized discrepancy detection
    def find_discrepancies(merged_df: pd.DataFrame) -> List[Dict]:
        """
        Efficiently find discrepancies across multiple columns.

        Args:
            merged_df (pd.DataFrame): Merged DataFrame of both files

        Returns:
            List of dictionaries containing discrepancy details
        """
        discrepancies = []
        columns_to_check = ['Charge', 'Stop_Date', 'New_Charge']

        for col in columns_to_check:
            ecb_col = col + '_ECB'
            tar_col = col + '_TAR'

            # Find rows with mismatched values
            mismatch_mask = merged_df[ecb_col] != merged_df[tar_col]
            mismatched_rows = merged_df[mismatch_mask]

            # Convert mismatches to list of discrepancy dictionaries
            for _, row in mismatched_rows.iterrows():
                discrepancies.append({
                    'Unique_Key': row['Unique_Key'],
                    'Column': col,
                    'ECB_Value': row[ecb_col],
                    'TAR_Value': row[tar_col]
                })

        return discrepancies

    # Generate discrepancies
    discrepancies_df = pd.DataFrame(find_discrepancies(merged))

    return discrepancies_df, missing_in_file1, missing_in_file2

def pretty_print_results(discrepancies: pd.DataFrame,
                         missing_in_file1: pd.DataFrame,
                         missing_in_file2: pd.DataFrame) -> None:
    """
    Prettify and print reconciliation results with formatted output.

    Args:
        discrepancies (pd.DataFrame): Discrepancies in matched transactions
        missing_in_file1 (pd.DataFrame): Transactions missing from first file
        missing_in_file2 (pd.DataFrame): Transactions missing from second file
    """
    # Custom print with tabulate for beautiful formatting
    print("\n--- Discrepancies in Matched Transactions ---")
    if not discrepancies.empty:
        print(tabulate(discrepancies, headers='keys', tablefmt='pretty', showindex=False))
    else:
        print("No discrepancies found in matched transactions.")

    print("\n--- Transactions Missing in ServiceCodes_ECB ---")
    if not missing_in_file1.empty:
        print(tabulate(missing_in_file1[['Spa', 'Service_Code']],
                       headers='keys', tablefmt='pretty', showindex=False))
    else:
        print("No transactions missing from ServiceCodes_ECB.")

    print("\n--- Transactions Missing in ServiceCodes_TAR ---")
    if not missing_in_file2.empty:
        print(tabulate(missing_in_file2[['Spa', 'Service_Code']],
                       headers='keys', tablefmt='pretty', showindex=False))
    else:
        print("No transactions missing from ServiceCodes_TAR.")

def main():
    """
    Main function to execute transaction record reconciliation.
    Handles file paths and calls reconciliation function.
    """
    try:
        # Update these paths to your actual file locations
        file1_path = 'ServiceCodes_ECB.csv'
        file2_path = 'ServiceCodes_TAR.csv'

        # Perform reconciliation
        discrepancies, missing_in_file1, missing_in_file2 = reconcile_transaction_records(
            file1_path, file2_path
        )

        # Pretty print results
        pretty_print_results(discrepancies, missing_in_file1, missing_in_file2)

        # Optional: Export results
        if not discrepancies.empty:
            discrepancies.to_csv('transaction_discrepancies.csv', index=False)
        if not missing_in_file1.empty:
            missing_in_file1.to_csv('missing_in_ECB.csv', index=False)
        if not missing_in_file2.empty:
            missing_in_file2.to_csv('missing_in_TAR.csv', index=False)

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except pd.errors.EmptyDataError:
        print("Error: One or both CSV files are empty.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()