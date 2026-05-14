package NucleusTeq.Capstone_EventTIcketBookingSystem.controller;

import org.springframework.security.access.prepost.PreAuthorize;

import org.springframework.web.bind.annotation.GetMapping;

import org.springframework.web.bind.annotation.RestController;

@RestController
public class CustomerController {

    @PreAuthorize("hasRole('CUSTOMER')")

    @GetMapping("/customer/book-ticket")

    public String bookTicket() {

        return "Ticket Booked Successfully";
    }
}