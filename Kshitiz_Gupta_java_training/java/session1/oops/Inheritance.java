package Kshitiz_Gupta_java_training.session1.oops;

public class Inheritance {
    public static void main(String[] args) {
        GraduateStudent s = new GraduateStudent("Kshitiz",92,101,2026,'A',false);
        s.displayDetails();
    }

    
}

class Student {
    String name;
    int marks;
    int rollno;

    Student(String name,int marks,int rollno) {
        this.name=name;
        this.marks=marks;
        this.rollno=rollno;
    }
}

class GraduateStudent extends Student {
    int yearOfPassing;
    char finalGrades;
    boolean duesClear;

    GraduateStudent(String name, int marks,int rollno,int yearOfPassing,char finalGrades,boolean duesClear) {
        super(name,marks,rollno);
        this.yearOfPassing=yearOfPassing;
        this.finalGrades=finalGrades;
        this.duesClear=duesClear;
    }

    void displayDetails() {
        System.out.println("Name: " + name);
        System.out.println("Roll No: " + rollno);
        System.out.println("Marks: " + marks);
        System.out.println("Year of Passing: " + yearOfPassing);
        System.out.println("Final Grade: " + finalGrades);
        System.out.println("Dues Cleared: " + duesClear);
    }
}

