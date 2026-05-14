package NucleusTeq.Capstone_EventTIcketBookingSystem.controller;

import org.springframework.security.access.prepost.PreAuthorize;

import org.springframework.web.bind.annotation.GetMapping;

import org.springframework.web.bind.annotation.RestController;

@RestController
public class OrganizerController {

    @PreAuthorize("hasRole('ORGANISER')")

    @GetMapping("/organizer/create-event")

    public String createEvent() {

        return "Event Created Successfully";
    }
}