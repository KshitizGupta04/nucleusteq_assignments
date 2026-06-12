package Kshitiz_Gupta_java_training.session1.StringManipulation;
import java.util.*;

public class VowelCount {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the String in lowercase");
        String str = sc.nextLine();

        int counta=0;
        int counte=0;
        int counti=0;
        int countu=0;
        int counto=0;
        for(int i=0;i<str.length();i++) {
            if(str.charAt(i)=='a') {
                counta++;
            }
            else if(str.charAt(i)=='e') {
                counte++;
            }
            else if(str.charAt(i)=='i') {
                counti++;
            }
            else if(str.charAt(i)=='o') {
                counto++;
            }
            else if(str.charAt(i)=='u') {
                countu++;
            }
        }

        System.out.println( "a " + counta);
        System.out.println( "e " + counte);
        System.out.println( "i " + counti);
        System.out.println( "o " + counto);
        System.out.println( "u " + countu);
    }
}
