package Kshitiz_Gupta_java_training.session1.AdvancedTopics;

public class Abstraction {
    public static void main(String[] args) {
        Dog d = new Dog();
        d.sound();
    }
}

abstract class Animal {
    abstract void sound();
    
    public void eat() {
        System.out.println("Animal eats");
    }
}

class Dog extends Animal {
    void sound() {
        System.out.println("Dog barks");
    }
}
