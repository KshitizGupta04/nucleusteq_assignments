"""
Assignment 5: Matplotlib Charts
"""

import matplotlib.pyplot as plt


class MatplotlibCharts:
    """Created basic charts using Matplotlib."""

    def __init__(self):
        self.departments = ["HR", "IT", "Finance"]
        self.employee_count = [5, 12, 7]
        self.salaries = [30000, 40000, 50000, 60000, 45000]
        self.ages = [25, 30, 28, 35, 29]

    def create_bar_chart(self):
        """to Display bar chart."""

        plt.figure(figsize=(6, 4))
        plt.bar(self.departments, self.employee_count)
        plt.title("Employees by Department")
        plt.xlabel("Department")
        plt.ylabel("Employees")
        plt.show()

    def create_line_chart(self):
        """to Display line chart."""

        plt.figure(figsize=(6, 4))
        plt.plot(self.departments, self.employee_count, marker="o")
        plt.title("Employees by Department")
        plt.xlabel("Department")
        plt.ylabel("Employees")
        plt.show()

    def create_histogram(self):
        """to Display salary histogram."""

        plt.figure(figsize=(6, 4))
        plt.hist(self.salaries, bins=5)
        plt.title("Salary Distribution")
        plt.xlabel("Salary")
        plt.ylabel("Frequency")
        plt.show()

    def create_scatter_plot(self):
        """to Display scatter plot."""

        plt.figure(figsize=(6, 4))
        plt.scatter(self.ages, self.salaries)
        plt.title("Age vs Salary")
        plt.xlabel("Age")
        plt.ylabel("Salary")
        plt.show()


def main():
    """Driver function."""

    try:
        charts = MatplotlibCharts()

        charts.create_bar_chart()
        charts.create_line_chart()
        charts.create_histogram()
        charts.create_scatter_plot()

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()