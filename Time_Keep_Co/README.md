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

## Development Approach

### Problem Understanding

The challenge was to create a tool that compares two transaction files (TAR and ECB) and identifies discrepancies. Here's how I approached it:

1. **Initial Analysis**
   - Examined sample files to understand data structure
   - Identified key fields that needed comparison
   - Determined possible types of discrepancies

2. **Design Decisions**
   - Chose Flask for its lightweight nature and quick setup
   - Used Bootstrap for responsive UI
   - Implemented client-side filtering for better user experience

### Implementation Strategy

1. **Data Processing Pipeline**

   ```
   File Upload → Data Loading → Cleaning → Comparison → Result Formation
   ```

2. **Key Components**
   - `data_loader.py`: Handles CSV parsing and initial structuring
   - `data_cleaner.py`: Normalizes dates and currency values
   - `comparator.py`: Core comparison logic
   - Web interface for user interaction

3. **Iterative Development**

   **Phase 1: Core Functionality**
   - Basic file upload
   - Simple comparison logic
   - Basic error handling

   **Phase 2: Enhanced Features**
   - Added data validation
   - Implemented detailed discrepancy reporting
   - Added error handling and logging

   **Phase 3: UI/UX Improvements**
   - Added filtering capabilities
   - Enhanced error messages
   - Improved result presentation
   - Added summary statistics

### Technical Challenges & Solutions

1. **Data Consistency**
   - **Challenge**: Inconsistent date and currency formats
   - **Solution**: Created dedicated cleaning functions in `data_cleaner.py`

2. **Performance**
   - **Challenge**: Large file processing
   - **Solution**: Optimized data structures using dictionary lookups

3. **User Experience**
   - **Challenge**: Complex data presentation
   - **Solution**: Implemented accordion-style UI with filtering

### Before vs After Comparison

**Before:**

- Manual file comparison
- Time-consuming process
- Prone to human error
- No standardized format

**After:**

- Automated comparison
- Instant results
- Standardized output
- Filterable results
- Clear discrepancy categorization
- Summary statistics

### Design Patterns Used

1. **Factory Pattern**
   - Used in app creation for better configuration management

2. **Strategy Pattern**
   - Implemented in comparator for different types of comparisons

3. **Builder Pattern**
   - Used in constructing discrepancy reports

### Future Improvements

1. **Performance Optimization**
   - Implement batch processing for larger files
   - Add caching for frequent comparisons

2. **Feature Enhancements**
   - Add export functionality
   - Implement detailed audit logging
   - Add custom comparison rules

3. **UI Improvements**
   - Add visualization of discrepancy patterns
   - Implement advanced filtering options
   - Add keyboard shortcuts
