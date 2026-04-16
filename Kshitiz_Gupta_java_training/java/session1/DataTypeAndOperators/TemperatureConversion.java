package Kshitiz_Gupta_java_training.session1.DataTypeAndOperators;
import java.util.*;

public class TemperatureConversion {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter 1 for converthing celsius to fahrenheit and 2 for coverting fahrenheit to celsius");
        int choice = sc.nextInt();

        switch(choice) {
            case 1 : System.out.println("Enter the temperature in celsius");
                double cel=sc.nextInt();
                System.out.println(celToFah(cel));
                break;
            
            case 2 : System.out.println("Enter the temperature in fahrenheit");
                double fah=sc.nextInt();
                System.out.println(fahToCel(fah));
                break;

            default : System.out.println("Invalid choice");
        }
    }
    public static double celToFah(double c) {
        return (9.0/5) * c + 32;
    }

    public static double fahToCel(double f) {
        return (5.0/9) * (f - 32);
    }
}
