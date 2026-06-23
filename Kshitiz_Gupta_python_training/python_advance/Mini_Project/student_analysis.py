"""
Assignment 7: Student Performance Analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class StudentPerformance:
    """to Perform student data analysis and visualization."""

    def create_dataframe(self):
        """tp Create student DataFrame."""

        student_data = {
            "Name": ["Rahul", "Priya", "Siri", "Anuj"],
            "Marks": [70, 80, 90, 60],
            "Hours Studied": [2, 3, 5, 1]
        }

        return pd.DataFrame(student_data)

    def add_performance(self, students):
        """to Add performance column."""

        students["Performance"] = students["Marks"].apply(
            lambda marks: "Pass" if marks > 65 else "Fail"
        )

        print("\nStudent Data:")
        print(students)

    def line_chart(self, students):
        """to Display line chart."""

        plt.figure(figsize=(6, 4))
        plt.plot(students["Hours Studied"], students["Marks"], marker="o")
        plt.title("Hours Studied vs Marks")
        plt.xlabel("Hours Studied")
        plt.ylabel("Marks")
        plt.grid(True)
        plt.show()

    def scatter_plot(self, students):
        """to Display scatter plot."""

        plt.figure(figsize=(6, 4))
        plt.scatter(students["Hours Studied"], students["Marks"])
        plt.title("Study Hours vs Marks")
        plt.xlabel("Hours Studied")
        plt.ylabel("Marks")
        plt.show()

    def bar_plot(self, students):
        """to Display performance bar plot."""

        plt.figure(figsize=(6, 4))
        sns.barplot(data=students, x="Performance", y="Marks")
        plt.title("Performance vs Marks")
        plt.show()


def main():
    """Driver function."""

    try:
        analysis = StudentPerformance()

        students = analysis.create_dataframe()

        analysis.add_performance(students)
        analysis.line_chart(students)
        analysis.scatter_plot(students)
        analysis.bar_plot(students)

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()