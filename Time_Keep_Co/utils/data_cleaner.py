def clean_currency(value):
    """Convert currency strings like ' $ 12.50 ' or '$12.00' to float, handle empty values"""
    if not value or value.strip() == '':
        return 0.0

    if isinstance(value, str):
        value = value.strip()
        if value.startswith("$"):
            value = value.replace("$", "").strip()
        try:
            return float(value) if value else 0.0
        except ValueError:
            print(f"Error: Invalid currency value: '{value}'")
            return 0.0
    return float(value) if value else 0.0


def clean_date(value):
    """Normalize date format MMDDYY"""
    if isinstance(value, str):
        value = value.strip()
        if len(value) == 6:  # Already in MMDDYY format
            return value
    return value
