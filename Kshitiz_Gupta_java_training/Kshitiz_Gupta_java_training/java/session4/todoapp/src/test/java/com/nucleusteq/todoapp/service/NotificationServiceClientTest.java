package com.nucleusteq.todoapp.service;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

class NotificationServiceClientTest {

    private final NotificationServiceClient service =
            new NotificationServiceClient();

    @Test
    void shouldSendNotification() {

        assertDoesNotThrow(() ->
                service.sendNotification("Test Notification"));
    }
}