class TransactionComparator:
    def __init__(self):
        self.discrepancies = []

    def add_discrepancy(
        self, disc_type, spa, service_code, tar_value=None, ecb_value=None
    ):
        self.discrepancies.append(
            {
                "type": disc_type,
                "spa": spa,
                "service_code": service_code,
                "tar_value": tar_value,
                "ecb_value": ecb_value,
            }
        )

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
                    self.add_discrepancy(
                        "charge_mismatch",
                        key[0],
                        key[1],
                        tar_record["Charge"],
                        ecb_record["Charge"],
                    )

                if tar_record["Stop Date"] != ecb_record["Stop Date"]:
                    self.add_discrepancy(
                        "stop_date_mismatch",
                        key[0],
                        key[1],
                        tar_record["Stop Date"],
                        ecb_record["Stop Date"],
                    )

                if (tar_record["New Charge"] or ecb_record["New Charge"]) and \
                   tar_record["New Charge"] != ecb_record["New Charge"]:
                    self.add_discrepancy(
                        "new_charge_mismatch",
                        key[0],
                        key[1],
                        tar_record["New Charge"],
                        ecb_record["New Charge"],
                    )

        # Check records in ECB missing from TAR
        for key in ecb_data:
            if key not in tar_data:
                self.add_discrepancy("missing_from_tar", key[0], key[1])

        return self.discrepancies


def format_discrepancies(discrepancies):
    formatted = []
    for d in discrepancies:
        item = {
            "type": d["type"],
            "spa": d["spa"],
            "service_code": d["service_code"],
            "tar_value": None,
            "ecb_value": None,
        }

        if d["type"] == "missing_from_ecb":
            item["title"] = "Transaction missing from ECB file"
        elif d["type"] == "missing_from_tar":
            item["title"] = "Transaction missing from TAR file"
        elif d["type"].endswith("_mismatch"):
            field = d["type"].replace("_mismatch", "").replace("_", " ").title()
            item.update(
                {
                    "title": f"{field} mismatch found",
                    "tar_value": format_value(d["tar_value"]),
                    "ecb_value": format_value(d["ecb_value"]),
                }
            )
        formatted.append(item)
    return formatted


def format_value(value):
    """Format values for display"""
    if isinstance(value, float):
        return f"${value:,.2f}"
    return str(value)
