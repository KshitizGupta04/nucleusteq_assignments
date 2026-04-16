package com.Kshitiz.java_training.component;

import org.springframework.stereotype.Component;

@Component("long")
public class LongMessageFormatter implements MessageFormatter {

    @Override
    public String format() {
        return "This is a long detailed message";
    }
}