package Kshitiz_Gupta_java_training.session1.StringManipulation;
import java.util.*;

public class Anagram {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter the First String");
        String str1=sc.nextLine();

        System.out.println("Enter the Second String");
        String str2=sc.nextLine();

        int[] freq1 = new int[26];
        for(int i=0;i<str1.length();i++) {
            freq1[str1.charAt(i)-'a']++;
        }

        int[] freq2 = new int[26];
        for(int i=0;i<str2.length();i++) {
            freq2[str2.charAt(i)-'a']++;
        }

        boolean flag=true;
        for(int i=0;i<26;i++) {
            if(freq1[i]!=freq2[i]) {
                flag=false;
                System.out.println("Not Anagrams");
                break;
            }
        }

        if(flag==true) {
            System.out.println("Strings are Anagram");
        }

    }
}
