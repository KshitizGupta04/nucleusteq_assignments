package Kshitiz_Gupta_java_training.session1.AdvancedTopics;

import java.io.*;

public class ReadData {
    public static void main(String[] args) {

        String fileName = "sample.txt";

        try {
            File file = new File(fileName);

            if (file.createNewFile()) {
                System.out.println("File created: " + file.getName());

                FileWriter writer = new FileWriter(file);
                writer.write("Hello Kshitiz \n Welcome to Java File Handling");
                writer.close();
            }

            BufferedReader br = new BufferedReader(new FileReader(file));
            String line;

            System.out.println("Reading file content:");
            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }

            br.close();

        } catch (IOException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}