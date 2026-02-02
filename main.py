import os
from datetime import datetime
from service.csv_handler import CSVHandler
from models.secret_santa import SecretSanta

def run_secret_santa():    
    filename = input("Enter current year employee list filename (e.g., employees.csv): ").strip()
    if not os.path.exists(filename):
        print(f"File '{filename}' not found.")
        return

    data = CSVHandler.read_csv(filename)
    required_columns = ['Employee_Name', 'Employee_EmailID']
    if not CSVHandler.validate_data(data, required_columns):
        return

    last_year_file = input("Enter last year's result filename (Optional, press Enter to skip): ").strip()
    last_year_data = []

    if last_year_file:
        if not os.path.exists(last_year_file):
            print(f"Last year's file '{last_year_file}' not found. Proceeding without it.")
        else:
            last_year_data = CSVHandler.read_csv(last_year_file)
            required_cols_prev = ['Employee_Name', 'Employee_EmailID', 'Secret_Child_Name', 'Secret_Child_EmailID']
            if not CSVHandler.validate_data(last_year_data, required_cols_prev):
                print("Invalid format in last year's data. Proceeding without it.")
                last_year_data = []

    assignment_result = SecretSanta.assign_santa(data, last_year_data)
    
    if assignment_result:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"secret_santa_result_{timestamp}.csv"
        CSVHandler.write_csv(output_file, assignment_result)
        print(f"Secret Santa result stored in '{output_file}'")
    else:
        print("Failed to generate a valid set of assignments.")

def main():
    try:        
        run_secret_santa()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
