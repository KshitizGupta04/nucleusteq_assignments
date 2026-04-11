package Kshitiz_Gupta_java_training.session1.basics;

import java.util.Scanner;

public class AreaCalculator {

    public double calculateCircleArea(double radius) {
        return Math.PI * radius * radius;
    }

    public double calculateRectangleArea(double length, double width) {
        return length * width;
    }

    public double calculateTriangleArea(double base, double height) {
        return 0.5 * base * height;
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        AreaCalculator ac = new AreaCalculator();

        System.out.println("Choose shape: 1.Circle 2.Rectangle 3.Triangle");
        int choice = sc.nextInt();

        switch (choice) {

            case 1:
                System.out.println("Enter radius:");
                double r = sc.nextDouble();
                System.out.println("Area: " + ac.calculateCircleArea(r));
                break;

            case 2:
                System.out.println("Enter length and width:");
                double l = sc.nextDouble();
                double w = sc.nextDouble();
                System.out.println("Area: " + ac.calculateRectangleArea(l, w));
                break;

            case 3:
                System.out.println("Enter base and height:");
                double b = sc.nextDouble();
                double h = sc.nextDouble();
                System.out.println("Area: " + ac.calculateTriangleArea(b, h));
                break;

            default:
                System.out.println("Invalid choice");
        }

        sc.close();
    }
}