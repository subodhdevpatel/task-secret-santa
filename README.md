# Secret Santa Assignment Tool

A Python-based Secret Santa assignment tool.

## Features

- **Constraint Fulfillment**: 
  - Each person is assigned exactly one unique recipient.
  - No self-assignments.
  - Optional: Avoid repeat assignments from the previous year.
- **Robust Validation**: 
  - Validates CSV structure and required columns.
  - Detects duplicate email addresses.
  - Ensures no empty values in required fields.
- **Auto-generated Results**: Saves timestamped output files to prevent overwriting.

## Project Structure

```text
secret-santa/
├── main.py              # Application entry point
├── models/
│   └── secret_santa.py  # Core assignment algorithm
├── service/
│   └── csv_handler.py   # CSV operations and data validation
├── employees.csv        # Example input file
└── README.md            # Documentation
```

## Setup & Running

1. **Prerequisites**: Python 3.8 or higher.
2. **Execute**:
   ```bash
   python main.py
   ```

## Data Format

### Current Employees (`employees.csv`)
Required columns:
- `Employee_Name`
- `Employee_EmailID`

### Historical Data (Optional)
Required columns from a previous result file:
- `Employee_Name`
- `Employee_EmailID`
- `Secret_Child_Name`
- `Secret_Child_EmailID`
