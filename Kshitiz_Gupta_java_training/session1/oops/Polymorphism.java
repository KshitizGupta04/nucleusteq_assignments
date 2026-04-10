package Kshitiz_Gupta_java_training.session1.oops;

public class Polymorphism {
    public static void main(String[] args) {
        Child c = new Child();
        System.out.println(c.add(5,6));
        System.out.println(c.add(5,6,7));
    }
}

class Parent {
    public int add(int num1,int num2) {
        return num1+num2;
    }
}

class Child extends Parent {
    public int add(int num1,int num2,int num3) {
        return num1+num2+num3;
    }
}
