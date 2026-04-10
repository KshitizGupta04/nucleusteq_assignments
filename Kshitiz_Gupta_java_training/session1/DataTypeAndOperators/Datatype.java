package Kshitiz_Gupta_java_training.session1.DataTypeAndOperators;

public class Datatype {
    public static void main(String[] args) {
        //in primitive data type they store the acutal value of the data
        int a=10;
        int b=a;
        b=20;
        System.out.println(a);
        
        //in reference data type they store the address of the data
        int[] arr={1,2,3};
        int[] arr2=arr;
        arr2[0]=7;
        System.out.println(arr[0]);
    }
}
