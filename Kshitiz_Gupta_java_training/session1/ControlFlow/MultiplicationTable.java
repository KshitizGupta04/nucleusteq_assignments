package Kshitiz_Gupta_java_training.session1.ControlFlow;
import java.util.*;

public class MultiplicationTable {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the number of which you want to print the table");
        int num=sc.nextInt();

        for(int i=1;i<=10;i++) {
            System.out.println(num*i);
        }
    }
}
