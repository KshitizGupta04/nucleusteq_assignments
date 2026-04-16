package com.Kshitiz.java_training.service;

import com.Kshitiz.java_training.component.MessageFormatter;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class MessageService {

    private final Map<String, MessageFormatter> formatterMap;

    public MessageService(Map<String, MessageFormatter> formatterMap) {
        this.formatterMap = formatterMap;
    }

    public String getMessage(String type) {
        MessageFormatter formatter = formatterMap.get(type.toLowerCase());

        if (formatter == null) {
            throw new RuntimeException("Invalid type");
        }

        return formatter.format();
    }
}