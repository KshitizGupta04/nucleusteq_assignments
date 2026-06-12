package Kshitiz_Gupta_java_training.session1.ControlFlow;
import java.util.*;

public class PrimeNumber {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the number");
        int n=sc.nextInt();
        boolean flag=true;

        for(int i=2;i<=Math.sqrt(i);i++) {
            if(n%i==0) {
                flag=false;
                System.out.println("Number is not prime");
            }
        }

        if(flag==true) {
            System.out.println("Number is prime");
        }
    }
}
