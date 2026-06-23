"""
Assignment 6: Seaborn Visualizations
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class SeabornCharts:
    """Create visualizations using Seaborn."""

    def __init__(self):
        self.employee_data = pd.DataFrame({
            "Name": ["Rahul", "Priya", "Amit", "Anuj"],
            "Age": [25, 30, 28, 35],
            "Department": ["HR", "IT", "Finance", "IT"],
            "Salary": [30000, 50000, 45000, 60000]
        })

    def create_barplot(self):
        """Display salary by department."""

        plt.figure(figsize=(6, 4))
        sns.barplot(data=self.employee_data, x="Department", y="Salary")
        plt.title("Department vs Salary")
        plt.show()

    def create_boxplot(self):
        """Display salary distribution."""

        plt.figure(figsize=(6, 4))
        sns.boxplot(data=self.employee_data, y="Salary")
        plt.title("Salary Distribution")
        plt.show()

    def create_heatmap(self):
        """Display correlation heatmap."""

        correlation = self.employee_data[["Age", "Salary"]].corr()

        plt.figure(figsize=(5, 4))
        sns.heatmap(correlation, annot=True, cmap="Blues")
        plt.title("Age and Salary Correlation")
        plt.show()


def main():
    """Driver function."""

    try:
        charts = SeabornCharts()

        charts.create_barplot()
        charts.create_boxplot()
        charts.create_heatmap()

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()