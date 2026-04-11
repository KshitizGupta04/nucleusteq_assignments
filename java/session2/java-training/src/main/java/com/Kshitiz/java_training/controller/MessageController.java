package com.Kshitiz.java_training.controller;

import com.Kshitiz.java_training.service.MessageService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/message")
public class MessageController {

    private final MessageService messageService;

    public MessageController(MessageService messageService) {
        this.messageService = messageService;
    }

    @GetMapping
    public String getMessage(@RequestParam String type) {
        return messageService.getMessage(type);
    }
}