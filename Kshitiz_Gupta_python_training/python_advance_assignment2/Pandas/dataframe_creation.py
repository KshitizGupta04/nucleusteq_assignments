"""
Assignment 2: Pandas DataFrame Creation
"""

import pandas as pd


class EmployeeDataFrame:
    """Create and perform operations on employee DataFrame."""

    def create_dataframe(self):
        """Create and return employee DataFrame."""

        employee_data = {
            "Name": ["Kshitiz", "Purnesh", "Kunjesh", "Darshan"],
            "Age": [25, 30, 28, 35],
            "Department": ["HR", "IT", "Finance", "IT"],
            "Salary": [30000, 50000, 45000, 60000]
        }

        return pd.DataFrame(employee_data)

    def display_first_two_rows(self, employee_dataframe):
        """Display first two rows."""

        print("\nFirst Two Rows:")
        print(employee_dataframe.head(2))

    def display_summary(self, employee_dataframe):
        """Display summary statistics."""

        print("\nSummary Statistics:")
        print(employee_dataframe.describe())

    def display_it_employees(self, employee_dataframe):
        """Display employees from IT department."""

        print("\nIT Employees:")
        print(employee_dataframe[employee_dataframe["Department"] == "IT"])

    def add_bonus_column(self, employee_dataframe):
        """Add bonus column."""

        employee_dataframe["Bonus"] = employee_dataframe["Salary"] * 0.10

        print("\nEmployee DataFrame with Bonus:")
        print(employee_dataframe)


def main():
    """Driver function."""

    try:
        employee = EmployeeDataFrame()

        employee_dataframe = employee.create_dataframe()

        print("Employee DataFrame:")
        print(employee_dataframe)

        employee.display_first_two_rows(employee_dataframe)
        employee.display_summary(employee_dataframe)
        employee.display_it_employees(employee_dataframe)
        employee.add_bonus_column(employee_dataframe)

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()