// Student Performance Analyzer

const students = [
  {
    name: "Lalit",
    marks: [
      { subject: "Math", score: 78 },
      { subject: "English", score: 82 },
      { subject: "Science", score: 74 },
      { subject: "History", score: 69 },
      { subject: "Computer", score: 88 }
    ],
    attendance: 82
  },
  {
    name: "Rahul",
    marks: [
      { subject: "Math", score: 90 },
      { subject: "English", score: 85 },
      { subject: "Science", score: 80 },
      { subject: "History", score: 76 },
      { subject: "Computer", score: 92 }
    ],
    attendance: 91
  }
];

function calculateTotal(student) {
  let total = 0;

  student.marks.forEach(mark => {
    total += mark.score;
  });

  return total;
}

function calculateAverage(total, count) {
  return total / count;
}

// Function to check fail conditions
function checkFail(student) {
  // Check subject fail
  for (let mark of student.marks) {
    if (mark.score <= 40) {
      return `Fail (Failed in ${mark.subject})`;
    }
  }

  // Check attendance
  if (student.attendance < 75) {
    return "Fail (Low Attendance)";
  }

  return null;
}

// Function to assign grade
function getGrade(avg) {
  if (avg >= 85) return "A";
  else if (avg >= 70) return "B";
  else if (avg >= 50) return "C";
  else return "Fail";
}
