package Kshitiz_Gupta_java_training.session1.StringManipulation;
import java.util.*;

public class ReverseString {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the String");
        String str = sc.nextLine();

        StringBuilder sb = new StringBuilder(str);
        int start=0;
        int end=str.length()-1;

        while(start<end) {
            char temp=sb.charAt(start);
            sb.setCharAt(start,sb.charAt(end));
            sb.setCharAt(end, temp);
            start++;
            end--;
        }

        System.out.println(sb);
    }
}
