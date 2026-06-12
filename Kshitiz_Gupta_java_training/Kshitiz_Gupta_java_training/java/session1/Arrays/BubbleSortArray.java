package Kshitiz_Gupta_java_training.session1.Arrays;
import java.util.*;

public class BubbleSortArray {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the size of the array");
        int size=sc.nextInt();
        int[] arr = new int[size];

        System.out.println("Enter the values in array");

        for(int i=0;i<size;i++) {
            arr[i]=sc.nextInt();
        }

        //bubble sort algorithm
        for(int i=0;i<size;i++) {
            for(int j=0;j<size-1-i;j++) {
                if(arr[j]>arr[j+1]) {
                    int temp=arr[j];
                    arr[j]=arr[j+1];
                    arr[j+1]=temp;
                }
            }
        }

        for(int i=0;i<size;i++) {
            System.out.println(arr[i]);
        }
    }
}
