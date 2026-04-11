package com.Kshitiz.java_training.component;

import org.springframework.stereotype.Component;

@Component
public class NotificationComponent {

    public String sendNotification() {
        return "Notification sent";
    }
}