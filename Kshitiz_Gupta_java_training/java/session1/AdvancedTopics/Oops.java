package Kshitiz_Gupta_java_training.session1.AdvancedTopics;

public class Oops {
    public static void main(String[] args) {
        Car c = new Car();
        c.start();
    }
}

interface Vehicle {
    void start();
}

class Car implements Vehicle {
    public void start() {
        System.out.println("Vehicle starts");
    }
}
