import pandas as pd
import numpy as np


def clean_amount(amount):
    if isinstance(amount, str):
        return float(amount.replace("$", "").replace(" ", "").strip())
    return amount


def compare_files(ecb_file, tar_file):
    try:
        # Read CSV files
        df_ecb = pd.read_csv(
            ecb_file, delimiter=",", skipinitialspace=True, on_bad_lines="skip"
        )

        df_tar = pd.read_csv(
            tar_file, delimiter=",", skipinitialspace=True, on_bad_lines="skip"
        )

        # Clean and standardize column names
        df_ecb.columns = [col.strip().replace(" ", "_") for col in df_ecb.columns]
        df_tar.columns = [col.strip().replace(" ", "_") for col in df_tar.columns]

        # Rename columns to match
        column_mapping = {"Service_Code": "Service_Code", "ServiceCode": "Service_Code"}
        df_ecb = df_ecb.rename(columns=column_mapping)
        df_tar = df_tar.rename(columns=column_mapping)

        # Clean data
        for df in [df_ecb, df_tar]:
            if "Charge" in df.columns:
                df["Charge"] = df["Charge"].apply(clean_amount)
            if "New_Charge" in df.columns:
                df["New_Charge"] = df["New_Charge"].apply(clean_amount)
            df["SPA"] = df["SPA"].str.strip()
            df["Service_Code"] = df["Service_Code"].str.strip()

        # Create unique keys
        df_ecb["key"] = df_ecb["SPA"] + "_" + df_ecb["Service_Code"]
        df_tar["key"] = df_tar["SPA"] + "_" + df_tar["Service_Code"]

        # Compare records
        ecb_keys = set(df_ecb["key"])
        tar_keys = set(df_tar["key"])

        print("\nDISCREPANCY REPORT")
        print("=" * 50)

        print(f"\nTotal records in ECB: {len(df_ecb)}")
        print(f"Total records in TAR: {len(df_tar)}")

        print("\nMissing in TAR file:")
        for key in ecb_keys - tar_keys:
            print(f"- {key}")

        print("\nMissing in ECB file:")
        for key in tar_keys - ecb_keys:
            print(f"- {key}")

        # Check for mismatches
        common_keys = ecb_keys.intersection(tar_keys)
        print("\nChecking value mismatches...")
        for key in common_keys:
            ecb_row = df_ecb[df_ecb["key"] == key].iloc[0]
            tar_row = df_tar[df_tar["key"] == key].iloc[0]

            if (
                ecb_row["Charge"] != tar_row["Charge"]
                or ecb_row["New_Charge"] != tar_row["New_Charge"]
            ):
                print(f"\nMismatch for {key}:")
                print(
                    f"ECB: Charge={ecb_row['Charge']}, New_Charge={ecb_row['New_Charge']}"
                )
                print(
                    f"TAR: Charge={tar_row['Charge']}, New_Charge={tar_row['New_Charge']}"
                )

    except Exception as e:
        print(f"Error processing files: {str(e)}")
        print(f"Available columns in ECB: {df_ecb.columns.tolist()}")
        print(f"Available columns in TAR: {df_tar.columns.tolist()}")


if __name__ == "__main__":
    compare_files("ServiceCodes_ECB.csv", "ServiceCodes_TAR.csv")
