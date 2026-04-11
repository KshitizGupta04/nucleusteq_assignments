package Kshitiz_Gupta_java_training.session1.Arrays;
import java.util.*;

public class LinearSearch {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter the size of array");
        int size=sc.nextInt();
        int[] arr = new int[size];

        System.out.println("Enter the values of array");
        for(int i=0;i<size;i++) {
            arr[i]=sc.nextInt();
        }

        System.out.println("Enter the target value");
        int target=sc.nextInt();

        boolean flag=false;
        for(int i=0;i<arr.length;i++) {
            if(arr[i]==target) {
                flag=true;
                System.out.println("The value is present at index " +i);
            }
        }

        if(flag==false) {
            System.out.println("Element not found");
        }
    }
}
