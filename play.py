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
        try:
            return float(value)
        except ValueError:
            print(f"Error: Invalid currency value: '{value}'")
            return 0.0
    return float(value)


def clean_date(value):
    """Normalize date format MMDDYY"""
    if isinstance(value, str):
        value = value.strip()
        if len(value) == 6:  # Already in MMDDYY format
            return value
        # Add more date format handling if needed
    return value


def load_tar_file(filepath):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, filepath)

        if not os.path.exists(full_path):
            print(f"Error: File not found: {full_path}")
            sys.exit(1)

        tar_data = {}
        with open(full_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    key = (row["SPA"].strip(), row["Service Code"].strip())
                    tar_data[key] = {
                        "Charge": clean_currency(row["Charge"]),
                        "Stop Date": clean_date(row["Stop Date"]),
                        "New Charge": clean_currency(row["New Charge"]),
                    }
                except KeyError as e:
                    print(f"Error: Missing column in TAR file: {e}")
                    print(f"Available columns: {list(row.keys())}")
                    sys.exit(1)
        return tar_data
    except Exception as e:
        print(f"Error reading TAR file: {str(e)}")
        sys.exit(1)


def load_ecb_file(filepath):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, filepath)

        if not os.path.exists(full_path):
            print(f"Error: File not found: {full_path}")
            sys.exit(1)

        ecb_data = {}
        with open(full_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    key = (row["SPA"].strip(), row["Service Code"].strip())
                    ecb_data[key] = {
                        "Charge": clean_currency(row["Charge"]),
                        "Stop Date": clean_date(row["Stop Date"]),
                        "New Charge": clean_currency(row["New Charge"]),
                        "Record Desc": row["Record Desc"].strip(),
                        "System": row["System"].strip(),
                        "Prin": row["Prin"].strip(),
                        "Agent": row["Agent"].strip(),
                    }
                except KeyError as e:
                    print(f"Error: Missing column in ECB file: {e}")
                    print(f"Available columns: {list(row.keys())}")
                    sys.exit(1)
        return ecb_data
    except Exception as e:
        print(f"Error reading ECB file: {str(e)}")
        sys.exit(1)


class TransactionComparator:
    def __init__(self):
        self.discrepancies = []

    def add_discrepancy(self, disc_type, spa, service_code, tar_value=None, ecb_value=None):
        self.discrepancies.append({
            "type": disc_type,
            "spa": spa,
            "service_code": service_code,
            "tar_value": tar_value,
            "ecb_value": ecb_value
        })

    def compare_files(self, tar_data, ecb_data):
        # Check records in TAR missing from ECB
        for key in tar_data:
            if key not in ecb_data:
                self.add_discrepancy("missing_from_ecb", key[0], key[1])
            else:
                # Compare fields that should match
                tar_record = tar_data[key]
                ecb_record = ecb_data[key]

                if tar_record["Charge"] != ecb_record["Charge"]:
                    self.add_discrepancy("charge_mismatch", key[0], key[1], tar_record["Charge"], ecb_record["Charge"])

                if tar_record["Stop Date"] != ecb_record["Stop Date"]:
                    self.add_discrepancy("stop_date_mismatch", key[0], key[1], tar_record["Stop Date"], ecb_record["Stop Date"])

                if tar_record["New Charge"] != ecb_record["New Charge"]:
                    self.add_discrepancy("new_charge_mismatch", key[0], key[1], tar_record["New Charge"], ecb_record["New Charge"])

        # Check records in ECB missing from TAR
        for key in ecb_data:
            if key not in tar_data:
                self.add_discrepancy("missing_from_tar", key[0], key[1])

        return self.discrepancies


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

    print("Loading and normalizing TAR file data...")
    tar_data = load_tar_file(tar_file)
    print(f"Loaded {len(tar_data)} records from TAR file")

    print("\nLoading and normalizing ECB file data...")
    ecb_data = load_ecb_file(ecb_file)
    print(f"Loaded {len(ecb_data)} records from ECB file")

    print("\nComparing normalized data...")
    comparator = TransactionComparator()
    discrepancies = comparator.compare_files(tar_data, ecb_data)
    print_discrepancies(discrepancies)


if __name__ == "__main__":
    main()
