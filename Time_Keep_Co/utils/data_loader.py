import csv
import os
from .data_cleaner import clean_currency, clean_date


def load_tar_file(filepath):
    tar_data = {}
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["SPA"].strip(), row["Service Code"].strip())
            tar_data[key] = {
                "Charge": clean_currency(row["Charge"]),
                "Stop Date": clean_date(row["Stop Date"]),
                "New Charge": clean_currency(row["New Charge"]),
            }
    return tar_data


def load_ecb_file(filepath):
    ecb_data = {}
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
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
    return ecb_data
