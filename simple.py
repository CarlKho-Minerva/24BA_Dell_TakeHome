import pandas as pd
import csv

def reconcile_transaction_records(file1_path, file2_path):
    """
    Reconcile transaction records between two CSV files.

    Args:
    file1_path (str): Path to the first CSV file (ServiceCodes_ECB)
    file2_path (str): Path to the second CSV file (ServiceCodes_TAR)

    Returns:
    tuple: Three DataFrames containing discrepancies and missing transactions
    """
    # Read CSV files with flexible parsing to handle potential formatting issues
    def read_csv_safely(file_path):
        with open(file_path, 'r') as f:
            # Detect dialect and handle potential extra whitespace
            dialect = csv.Sniffer().sniff(f.read(1024))
            f.seek(0)

        # Read with more robust parsing
        df = pd.read_csv(
            file_path,
            dialect=dialect,
            skipinitialspace=True,  # Remove leading whitespace
            dtype=str  # Read all columns as strings to prevent type conversion issues
        )

        # Strip whitespace from column names
        df.columns = df.columns.str.strip()

        return df

    # Read both files
    df1 = read_csv_safely(file1_path)
    df2 = read_csv_safely(file2_path)

    # Create unique keys for matching
    df1['unique_key'] = df1['SPA'] + '_' + df1['Service Code']
    df2['unique_key'] = df2['SPA'] + '_' + df2['Service Code']

    # Identify missing transactions
    missing_in_file1 = df2[~df2['unique_key'].isin(df1['unique_key'])]
    missing_in_file2 = df1[~df1['unique_key'].isin(df2['unique_key'])]

    # Find matched transactions with discrepancies
    # Merge files on unique key to compare other fields
    merged = pd.merge(df1, df2, on='unique_key', suffixes=('_ECB', '_TAR'))

    # Identify transactions with mismatched data
    discrepancies = []
    columns_to_check = ['Charge', 'Stop Date', 'New Charge']

    for _, row in merged.iterrows():
        row_discrepancies = []
        for col in columns_to_check:
            ecb_col = col + '_ECB'
            tar_col = col + '_TAR'

            # Compare values, handling potential formatting differences
            if str(row[ecb_col]).strip() != str(row[tar_col]).strip():
                row_discrepancies.append({
                    'Unique Key': row['unique_key'],
                    'Column': col,
                    'ECB Value': row[ecb_col],
                    'TAR Value': row[tar_col]
                })

        if row_discrepancies:
            discrepancies.extend(row_discrepancies)

    # Convert discrepancies to DataFrame for easy viewing
    discrepancies_df = pd.DataFrame(discrepancies)

    return discrepancies_df, missing_in_file1, missing_in_file2

def main():
    # Paths to the input files (replace with actual file paths)
    file1_path = 'ServiceCodes_ECB.csv'
    file2_path = 'ServiceCodes_TAR.csv'

    # Perform reconciliation
    discrepancies, missing_in_file1, missing_in_file2 = reconcile_transaction_records(file1_path, file2_path)

    # Output results
    print("\n--- Discrepancies in Matched Transactions ---")
    if not discrepancies.empty:
        print(discrepancies)
    else:
        print("No discrepancies found in matched transactions.")

    print("\n--- Transactions Missing in ServiceCodes_ECB ---")
    if not missing_in_file1.empty:
        print(missing_in_file1[['SPA', 'Service Code']])
    else:
        print("No transactions missing from ServiceCodes_ECB.")

    print("\n--- Transactions Missing in ServiceCodes_TAR ---")
    if not missing_in_file2.empty:
        print(missing_in_file2[['SPA', 'Service Code']])
    else:
        print("No transactions missing from ServiceCodes_TAR.")

    # Optional: Export results to CSV files for further analysis
    if not discrepancies.empty:
        discrepancies.to_csv('transaction_discrepancies.csv', index=False)
    if not missing_in_file1.empty:
        missing_in_file1.to_csv('missing_in_ECB.csv', index=False)
    if not missing_in_file2.empty:
        missing_in_file2.to_csv('missing_in_TAR.csv', index=False)

if __name__ == '__main__':
    main()