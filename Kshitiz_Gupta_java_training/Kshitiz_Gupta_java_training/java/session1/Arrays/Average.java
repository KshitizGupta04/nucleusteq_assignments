package Kshitiz_Gupta_java_training.session1.Arrays;
import java.util.*;

public class Average {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter the size of array");
        int n=sc.nextInt();
        int[] arr = new int[n];

        System.out.println("Enter the values of array");
        for(int i=0;i<n;i++) {
            arr[i]=sc.nextInt();
        }

        double sum=0;
        for(int i=0;i<arr.length;i++) {
            sum=sum+arr[i];
        }
        System.out.println(sum/(double)arr.length);
    }
}
