package Kshitiz_Gupta_java_training.session1.Arrays;
import java.util.*;

public class SelectionSortArray {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter the size of array");
        int size=sc.nextInt();
        int[] arr = new int[size];

        System.out.println("Enter the values of array");
        for(int i=0;i<size;i++) {
            arr[i]=sc.nextInt();
        }

        for(int i = 0; i < size - 1; i++) {
            int minIndex = i;
            for(int j = i + 1; j < size; j++) {
                if(arr[j] < arr[minIndex]) {
                    minIndex = j;
                }
            }
            int temp = arr[i];
            arr[i] = arr[minIndex];
            arr[minIndex] = temp;
        }

        for(int val:arr) {
            System.out.println(val);
        }
    }
}
