package Kshitiz_Gupta_java_training.session1.basics;
import java.util.*;

public class Loops {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter 1 for triangle and 2 for square");
        int choice=sc.nextInt();

        switch(choice) {
            case 1: System.out.println("enter the number of lines");
                    int n=sc.nextInt();
                    for(int i=1;i<=n;i++) {
                        for(int j=1;j<=i;j++) {
                            System.out.print("* ");
                        }
                        System.out.println();
                    }
                    break;
            
            case 2: System.out.println("enter the number of lines");
                    int n2=sc.nextInt();
                    for(int i=1;i<=n2;i++) {
                        for(int j=1;j<=n2;j++) {
                            System.out.print("*");
                        }
                        System.out.println();
                    }
                    break;

            default : System.out.println("Invalid choice");
        }
    }
}
