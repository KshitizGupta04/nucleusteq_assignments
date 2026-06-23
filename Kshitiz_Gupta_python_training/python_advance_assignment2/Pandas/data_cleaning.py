"""
Assignment 3: Data Cleaning
"""

import numpy as np
import pandas as pd


class EmployeeDataCleaner:
    """Perform data cleaning operations."""

    def create_dataframe(self):
        """Create DataFrame containing missing values."""

        employee_data = {
            "Name": ["Rahul", "Priya", "Anuj"],
            "Age": [25, np.nan, 29],
            "Salary": [30000, 40000, np.nan]
        }

        return pd.DataFrame(employee_data)

    def show_missing_values(self, employees):
        """Display missing values."""

        print("Missing Values:")
        print(employees.isnull())

    def fill_missing_age(self, employees):
        """Replace missing age with average age."""

        average_age = employees["Age"].mean()
        employees["Age"] = employees["Age"].fillna(average_age)

    def fill_missing_salary(self, employees):
        """Replace missing salary with zero."""

        employees["Salary"] = employees["Salary"].fillna(0)

    def display_dataframe(self, employees):
        """Display cleaned DataFrame."""

        print("\nCleaned Data:")
        print(employees)


def main():

    try:
        cleaner = EmployeeDataCleaner()

        employees = cleaner.create_dataframe()

        cleaner.show_missing_values(employees)
        cleaner.fill_missing_age(employees)
        cleaner.fill_missing_salary(employees)
        cleaner.display_dataframe(employees)

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()