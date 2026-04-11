package Kshitiz_Gupta_java_training.session1.ControlFlow;
import java.util.*;

public class Evensum {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int i=1;
        int sum=0;
        while(i<=10) {
            if(i%2==0) {
                sum=sum+i;
            }
            i++;
        }
        System.out.println(sum);
    }
}
