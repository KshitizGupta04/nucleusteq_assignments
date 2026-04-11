package Kshitiz_Gupta_java_training.session1.basics;
import java.util.*;

public class Factorial {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the number");
        int num=sc.nextInt();

        int prod=1;
        for(int i=1;i<=num;i++) {
            prod=prod*i;
        }
        System.out.println("The factorial is" + " " +prod);
        sc.close();
    }
}
