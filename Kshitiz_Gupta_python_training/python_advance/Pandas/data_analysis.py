"""
Assignment 4: Data Analysis
"""

import pandas as pd


class EmployeeAnalysis:
    """Perform analysis on employee data."""

    def create_dataframe(self):
        """Create employee DataFrame."""

        employee_details = {
            "Name": ["Rahul", "Priya", "Amit", "Anuj"],
            "Age": [25, 30, 28, 35],
            "Department": ["HR", "IT", "Finance", "IT"],
            "Salary": [30000, 50000, 45000, 60000]
        }

        return pd.DataFrame(employee_details)

    def average_salary(self, employees):
        """to Display average salary by department."""

        print("\nAverage Salary by Department:")
        print(employees.groupby("Department")["Salary"].mean())

    def highest_salary(self, employees):
        """ to Display maximum salary by department."""

        print("\nMaximum Salary by Department:")
        print(employees.groupby("Department")["Salary"].max())

    def employee_count(self, employees):
        """to Display employee count by department."""

        print("\nEmployee Count by Department:")
        print(employees.groupby("Department")["Name"].count())


def main():
    """Driver function."""

    try:
        analysis = EmployeeAnalysis()

        employees = analysis.create_dataframe()

        analysis.average_salary(employees)
        analysis.highest_salary(employees)
        analysis.employee_count(employees)

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()