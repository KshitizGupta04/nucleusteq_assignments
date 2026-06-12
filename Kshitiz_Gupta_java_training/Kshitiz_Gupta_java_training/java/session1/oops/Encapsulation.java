package Kshitiz_Gupta_java_training.session1.oops;

public class Encapsulation {
    public static void main(String[] args) {
        Demo d = new Demo();  
        d.setPassword(123456);
        System.out.println(d.getPassword());
    }
}

class Demo {
    private int password;

    // Getter
    public int getPassword() {
        return this.password;
    }

    // Setter
    public void setPassword(int password) {
        this.password = password;
    }
}