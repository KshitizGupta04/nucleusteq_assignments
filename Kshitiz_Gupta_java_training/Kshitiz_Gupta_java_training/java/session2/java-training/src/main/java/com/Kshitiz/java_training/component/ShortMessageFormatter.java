package com.Kshitiz.java_training.component;

import org.springframework.stereotype.Component;

@Component("short")
public class ShortMessageFormatter implements MessageFormatter {

    @Override
    public String format() {
        return "Short Message";
    }
}