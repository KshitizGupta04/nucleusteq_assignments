package com.Kshitiz.java_training.service;

import com.Kshitiz.java_training.component.NotificationComponent;
import org.springframework.stereotype.Service;

@Service
public class NotificationService {

    private final NotificationComponent notificationComponent;

    public NotificationService(NotificationComponent notificationComponent) {
        this.notificationComponent = notificationComponent;
    }

    public String triggerNotification() {
        return notificationComponent.sendNotification();
    }
}