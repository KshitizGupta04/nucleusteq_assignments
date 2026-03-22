# Student Performance Analyzer

## Description
This project is a console-based JavaScript application that analyzes student performance using arrays and objects. It calculates total marks, averages, subject-wise statistics, and determines the class topper.

---

## Features
- Total marks calculation for each student  
- Average marks calculation  
- Subject-wise highest score  
- Subject-wise average score  
- Class topper identification  
- Grade assignment system  
- Fail conditions (low marks / low attendance)  

---

## Technologies Used
- JavaScript (Core Fundamentals)
- Console Output (No DOM)

---

## Output Screenshot

This screenshot shows the program output including total marks, average, grades, and topper:

![Program Output](output1_image.png)

---

## 🧠 Logic Explanation

### 🔹 Data Structure
- Used an **array of objects** to store student details.
- Each student contains:
  - Name
  - Marks (array of subjects)
  - Attendance

### 🔹 Calculations
- Used **loops (forEach, for)** to iterate through data.
- Created **functions** for:
  - Total marks
  - Average calculation
  - Grade assignment
  - Fail condition checking


### 🔹 Fail Conditions
- Any subject score ≤ 40  
- Attendance < 75%  

---

## Output Highlights
- Displays total and average marks for each student  
- Shows subject-wise highest and average scores  
- Identifies the class topper  
- Assigns grades based on performance  

---
