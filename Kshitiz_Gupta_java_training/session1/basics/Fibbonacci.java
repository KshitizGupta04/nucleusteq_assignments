package Kshitiz_Gupta_java_training.session1.basics;
import java.util.*;

public class Fibbonacci {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the number");
        int num=sc.nextInt();
        System.out.println(fib(num));
        sc.close();
    }

    public static int fib(int n) {
        if(n==0 || n==1) {
            return n;
        }
        int val=fib(n-1)+fib(n-2);
        return val;
    }
}
