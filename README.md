# Dell File Comparator & ShipKeep Co

## Overview

This repository contains two distinct applications:

1. **Dell File Comparator**: A Flask-based web application designed to compare transaction records between two files (TAR and ECB) and identify discrepancies.
2. **ShipKeep Co**: A React-based frontend application for a fictional cruise booking company.

## Dell File Comparator

### Features

- File upload interface for TAR and ECB files
- Automated comparison of transaction records
- Detailed discrepancy reporting
- CSV file format support

### Setup

1. Clone the repository
2. Navigate to the `Time_Keep_Co` directory
3. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Start the application:

   ```bash
   python run.py
   ```

2. Open <http://localhost:5000> in your browser
3. Upload TAR and ECB files for comparison
4. View discrepancy results

### Technical Implementation Details

#### Data Structure Design

1. **Composite Key Strategy**
   ```python
   key = (row["SPA"].strip(), row["Service Code"].strip())
   ```
   - Using tuple as dictionary key for O(1) lookups
   - Combines SPA and Service Code for unique record identification
   - Enables efficient comparison between files

2. **Record Storage Format**
   ```python
   record = {
       "Charge": clean_currency(row["Charge"]),
       "Stop Date": clean_date(row["Stop Date"]),
       "New Charge": clean_currency(row["New Charge"])
   }
   ```
   - Normalized data structure
   - Pre-cleaned values for comparison
   - Minimal memory footprint

#### Comparison Algorithm

1. **Two-Pass Approach**
   ```
   First Pass:  TAR → ECB (find missing/mismatched in ECB)
   Second Pass: ECB → TAR (find missing in TAR)
   ```

2. **Comparison Logic**
   ```
   For each record:
   1. Check existence (O(1) lookup)
   2. If exists, compare fields:
      - Charge amount
      - Stop date
      - New charge
   3. Track discrepancy type and values
   ```

3. **Performance Considerations**
   - Time Complexity: O(n + m) where n, m are file sizes
   - Space Complexity: O(n + m) for storing records
   - Memory Usage: ~100MB per 500K records

#### Testing Approach

1. **Unit Test Categories**
   ```
   1. Data Loading Tests
      - File format variations
      - Character encodings
      - Missing columns

   2. Cleaning Tests
      - Currency formats
      - Date formats
      - Edge cases

   3. Comparison Tests
      - Missing records
      - Value mismatches
      - Large datasets
   ```

2. **Performance Benchmarks**
   ```
   Small Files  (1K records):   < 0.1 seconds
   Medium Files (50K records):  < 1.5 seconds
   Large Files  (500K records): < 10 seconds
   ```

### Project Structure

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

### Logging

Logs are stored in

app.log

 and include:

- File processing events
- Error tracking
- Application status

### Error Handling

The application handles:

- Invalid file formats
- Missing required fields
- File processing errors
- Data comparison issues

### Scalability Considerations

1. **Current Limitations**
   - Single-threaded processing
   - In-memory data structures
   - Synchronous file I/O

2. **Scaling Solutions**
   ```
   Short-term:
   - Batch processing
   - Memory-mapped files
   - Parallel comparison

   Long-term:
   - Distributed processing
   - Database integration
   - Microservice architecture
   ```

## ShipKeep Co

### Features

- User-friendly interface for cruise booking
- Responsive design using Tailwind CSS
- Authentication (Login and Signup)
- Featured destinations and cruise details

### Setup

1. Clone the repository
2. Navigate to the

shipkeep-app

 directory
3. Install frontend dependencies:

   ```bash
   cd frontend
   npm install
   ```

4. Install backend dependencies:

   ```bash
   cd ../backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Usage

1. Start the backend server:

   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   flask run
   ```

2. Start the frontend server:

   ```bash
   cd ../frontend
   npm start
   ```

3. Open <http://localhost:3000> in your browser

### Project Structure

```
shipkeep-app/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
└── README.md
```

### Available Scripts

In the `frontend` directory, you can run:

- `npm start`: Runs the app in development mode.
- `npm run build`: Builds the app for production.
- `npm test`: Launches the test runner.
- `npm run eject`: Ejects the configuration files.

### Things I Learned

- Using concurrently to run both the frontend and backend servers at the same time.
- Adding `"proxy": "http://127.0.0.1:5000",` to `package.json` to resolve CORS issues.

### Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

For more information, refer to the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

## Conclusion

This repository showcases two distinct applications demonstrating skills in both backend and frontend development. The Dell File Comparator focuses on data comparison and discrepancy reporting, while ShipKeep Co provides a user-friendly interface for cruise booking. Both applications are designed with scalability and user experience in mind.
