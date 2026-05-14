package NucleusTeq.Capstone_EventTIcketBookingSystem.controller;

import org.springframework.web.bind.annotation.GetMapping;

import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {

    @GetMapping("/test")

    public String testApi() {
        return "Protected API Accessed Successfully";
    }
}