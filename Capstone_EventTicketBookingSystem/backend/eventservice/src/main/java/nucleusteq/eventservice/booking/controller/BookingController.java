package nucleusteq.eventservice.booking.controller;

import nucleusteq.eventservice.booking.dto.BookingRequestDTO;
import nucleusteq.eventservice.booking.entity.Booking;
import nucleusteq.eventservice.booking.service.BookingService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/bookings")
public class BookingController {

    private final BookingService bookingService;

    public BookingController(BookingService bookingService) {
        this.bookingService = bookingService;
    }

    @PreAuthorize("hasRole('CUSTOMER')")
    @PostMapping
    public ResponseEntity<String> bookTickets(@Valid @RequestBody BookingRequestDTO requestDTO, Authentication authentication) {
        return ResponseEntity.ok(bookingService.bookTickets(requestDTO, authentication.getName()));
    }

    @PreAuthorize("hasRole('CUSTOMER')")
    @GetMapping("/my-bookings")
    public ResponseEntity<List<Booking>> getMyBookings(Authentication authentication) {
        return ResponseEntity.ok(bookingService.getMyBookings(authentication.getName()));
    }

    @PreAuthorize("hasRole('CUSTOMER')")
    @DeleteMapping("/{id}")
    public ResponseEntity<String> cancelBooking(@PathVariable Long id, Authentication authentication) {
        return ResponseEntity.ok(bookingService.cancelBooking(id, authentication.getName()));
    }
}