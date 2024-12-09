import pandas as pd
import os
import csv
import sys


def clean_currency(value):
    """Convert currency strings like ' $ 12.50 ' or '$12.00' to float"""
    if isinstance(value, str):
        value = value.strip()
        if value.startswith("$"):
            value = value.replace("$", "").strip()
        return float(value)
    return float(value)


def load_tar_file(filepath):
    tar_data = {}
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['SPA'], row['Service Code'])
            tar_data[key] = {
                'Charge': row['Charge'],
                'Stop Date': row['Stop Date'],
                'New Charge': row['New Charge']
            }
    return tar_data


def load_ecb_file(filepath):
    ecb_data = {}
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['SPA'], row['Service Code'])
            ecb_data[key] = {
                'Charge': row['Charge'],
                'Stop Date': row['Stop Date'],
                'New Charge': row['New Charge']
            }
    return ecb_data


def compare_files(tar_data, ecb_data):
    discrepancies = []

    # Check records in TAR missing from ECB
    for key in tar_data:
        if key not in ecb_data:
            discrepancies.append(
                {"type": "missing_from_ecb", "spa": key[0], "service_code": key[1]}
            )
        else:
            # Compare fields that should match
            tar_record = tar_data[key]
            ecb_record = ecb_data[key]

            if tar_record["Charge"] != ecb_record["Charge"]:
                discrepancies.append(
                    {
                        "type": "charge_mismatch",
                        "spa": key[0],
                        "service_code": key[1],
                        "tar_value": tar_record["Charge"],
                        "ecb_value": ecb_record["Charge"],
                    }
                )

            if tar_record["Stop Date"] != ecb_record["Stop Date"]:
                discrepancies.append(
                    {
                        "type": "stop_date_mismatch",
                        "spa": key[0],
                        "service_code": key[1],
                        "tar_value": tar_record["Stop Date"],
                        "ecb_value": ecb_record["Stop Date"],
                    }
                )

            if tar_record["New Charge"] != ecb_record["New Charge"]:
                discrepancies.append(
                    {
                        "type": "new_charge_mismatch",
                        "spa": key[0],
                        "service_code": key[1],
                        "tar_value": tar_record["New Charge"],
                        "ecb_value": ecb_record["New Charge"],
                    }
                )

    # Check records in ECB missing from TAR
    for key in ecb_data:
        if key not in tar_data:
            discrepancies.append(
                {"type": "missing_from_tar", "spa": key[0], "service_code": key[1]}
            )

    return discrepancies


def print_discrepancies(discrepancies):
    print("\nDiscrepancy Report:")
    print("-" * 80)

    for d in discrepancies:
        if d["type"] == "missing_from_ecb":
            print(f"Transaction missing from ECB file:")
            print(f"    SPA: {d['spa']}")
            print(f"    Service Code: {d['service_code']}")

        elif d["type"] == "missing_from_tar":
            print(f"Transaction missing from TAR file:")
            print(f"    SPA: {d['spa']}")
            print(f"    Service Code: {d['service_code']}")

        elif d["type"].endswith("_mismatch"):
            field = d["type"].replace("_mismatch", "").replace("_", " ").title()
            print(f"{field} mismatch found:")
            print(f"    SPA: {d['spa']}")
            print(f"    Service Code: {d['service_code']}")
            print(f"    TAR value: {d['tar_value']}")
            print(f"    ECB value: {d['ecb_value']}")
        print("-" * 80)


def main():
    tar_file = "ServiceCodes_TAR.csv"
    ecb_file = "ServiceCodes_ECB.csv"

    print("Loading TAR file...")
    tar_data = load_tar_file(tar_file)
    print(f"Loaded {len(tar_data)} records from TAR file")

    print("\nLoading ECB file...")
    ecb_data = load_ecb_file(ecb_file)
    print(f"Loaded {len(ecb_data)} records from ECB file")

    print("\nComparing files...")
    discrepancies = compare_files(tar_data, ecb_data)
    print_discrepancies(discrepancies)


if __name__ == "__main__":
    main()
