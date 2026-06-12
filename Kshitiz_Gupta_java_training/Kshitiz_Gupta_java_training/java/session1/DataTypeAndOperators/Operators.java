package Kshitiz_Gupta_java_training.session1.DataTypeAndOperators;
import java.util.*;

public class Operators {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter the first no");
        int num1=sc.nextInt();

        System.out.println("Enter the second no");
        int num2=sc.nextInt();

        //Arithmetic operators
        System.out.println("Arithmetic operations results are:-");
        System.out.println("Addition " + (num1+num2));
        System.out.println("Subtraction " + (num1-num2));
        System.out.println("Multiplication " + (num1*num2));
        System.out.println("Modulas " + (num1%num2));

        if(num2!=0) System.out.println("Division " + num1/num2);
        else System.out.println("Wrong input value for division");

        //Relatioal operator
        System.out.println("Relational operators results are:-");
        System.out.println(num1==num2);
        System.out.println(num1>=num2);
        System.out.println(num1<=num2);
        System.out.println(num1>num2);
        System.out.println(num1<num2);
        System.out.println(num1!=num2);

        //logical operators
        System.out.println("logical operators results are:-");
        System.out.println(num1>0 && num2>0);
        System.out.println(num1>0 || num2>0);
        System.out.println(!(num1>0));

    }
}
