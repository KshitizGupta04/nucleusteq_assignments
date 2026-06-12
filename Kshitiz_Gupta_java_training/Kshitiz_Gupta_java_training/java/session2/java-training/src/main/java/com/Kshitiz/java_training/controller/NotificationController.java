package com.Kshitiz.java_training.controller;

import com.Kshitiz.java_training.service.NotificationService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/notify")
public class NotificationController {

    private final NotificationService notificationService;

    public NotificationController(NotificationService notificationService) {
        this.notificationService = notificationService;
    }

    @GetMapping
    public String sendNotification() {
        return notificationService.triggerNotification();
    }
}