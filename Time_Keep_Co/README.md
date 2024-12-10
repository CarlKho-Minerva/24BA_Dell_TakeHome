# Dell File Comparator

A Flask-based web application for comparing TAR and ECB transaction files.

## Features

- File upload interface for TAR and ECB files
- Automated comparison of transaction records
- Detailed discrepancy reporting
- CSV file format support

## Setup

1. Clone the repository
2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:

   ```bash
   python run.py
   ```

2. Open <http://localhost:5000> in your browser
3. Upload TAR and ECB files for comparison
4. View discrepancy results

## File Format Requirements

### TAR File Columns

- SPA
- Service Code
- Charge
- Stop Date
- New Charge

### ECB File Columns

- SPA
- Service Code
- Charge
- Stop Date
- New Charge
- Record Desc
- System
- Prin
- Agent

## Project Structure

```
Time_Keep_Co/
├── app/
│   ├── templates/
│   ├── __init__.py
│   └── routes.py
├── utils/
│   ├── data_loader.py
│   ├── data_cleaner.py
│   └── comparator.py
├── config.py
├── run.py
└── README.md
```

## Logging

Logs are stored in `app.log` and include:

- File processing events
- Error tracking
- Application status

## Error Handling

The application handles:

- Invalid file formats
- Missing required fields
- File processing errors
- Data comparison issues

## Interpreting Results

The application reports several types of discrepancies between TAR and ECB files:

| Discrepancy Type | Description | Example |
|-----------------|-------------|---------|
| Missing from ECB | Record exists in TAR but not in ECB | `SPA: 815530000300, Service Code: DF001` |
| Missing from TAR | Record exists in ECB but not in TAR | `SPA: 815530000300, Service Code: DF001` |
| Charge mismatch | Different charge amounts between files | `TAR: $100.00, ECB: $150.00` |
| Stop Date mismatch | Different stop dates between files | `TAR: 063023, ECB: 063024` |
| New Charge mismatch | Different new charge amounts | `TAR: $200.00, ECB: $250.00` |

Example discrepancy output:

## Understanding Comparison Results

The application provides detailed discrepancy reports in the following categories:

### Quick Summary
| Result Type | Description | Action Needed |
|------------|-------------|---------------|
| New Charge mismatch | Different charge amounts between TAR and ECB | Review charge differences |
| Missing from TAR | Record exists in ECB but not in TAR | Check for missing TAR entries |
| Missing from ECB | Record exists in TAR but not in ECB | Check for missing ECB entries |

### Common Patterns

1. **Service Code Groups**
   - VP001, VP068, VP227, VP324: Often appear together for the same SPA
   - Missing entries often occur in groups of related service codes

2. **SPA Number Structure**
   - Format: 8155XXXXXXXX
   - Special formats:
     - TOT entries (e.g., 81557000TOT)
     - System totals (e.g., 8155SYS TOT)

3. **Example Interpretation**
