import csv
import os
from typing import List, Dict, Any

class CSVHandler:
    """
    Handles CSV file operations including reading, writing, and data validation.
    """

    @staticmethod
    def read_csv(file_path: str) -> List[Dict[str, Any]]:
        """
        Reads a CSV file and returns the content as a list of dictionaries.
        
        Args:
            file_path: Path to the CSV file.
            
        Returns:
            A list of dictionaries representing the CSV rows.
        """
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return []

        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = [row for row in reader]
                return data
        except Exception as e:
            print(f"Error: Failed to read CSV file '{file_path}': {e}")
            return []

    @staticmethod
    def write_csv(file_path: str, data: List[Dict[str, Any]]):
        """
        Writes a list of dictionaries to a CSV file.
        
        Args:
            file_path: Destination path for the CSV file.
            data: List of dictionaries to write.
        """
        if not data:
            print("Error: No data provided to write.")
            return

        try:
            headers = data[0].keys()
            with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            print(f"Error: Failed to write to CSV file '{file_path}': {e}")

    @staticmethod
    def validate_data(data: List[Dict[str, Any]], required_columns: List[str]) -> bool:
        """
        Validates that the data contains required columns and no empty values.
        Also checks for duplicate email addresses.
        
        Args:
            data: Data to validate.
            required_columns: Columns that must be present in each row.
            
        Returns:
            True if data is valid, False otherwise.
        """
        if not data:
            print("Error: Data is empty.")
            return False

        required_set = set(required_columns)
        emails_seen = set()
        
        for index, row in enumerate(data):
            # Check for missing columns
            missing = required_set - row.keys()
            if missing:
                print(f"Error at Row {index + 1}: Missing columns {missing}")
                return False
            
            # Check for empty values and duplicate emails
            for col in required_columns:
                val = str(row.get(col, '')).strip()
                if not val:
                    print(f"Error at Row {index + 1}: {col} is empty.")
                    return False
                
                if col == 'Employee_EmailID':
                    if val in emails_seen:
                        print(f"Error at Row {index + 1}: Duplicate email address '{val}' found.")
                        return False
                    emails_seen.add(val)
                
        return True
