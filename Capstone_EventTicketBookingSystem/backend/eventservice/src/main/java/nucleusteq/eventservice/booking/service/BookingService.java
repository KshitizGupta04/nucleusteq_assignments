package nucleusteq.eventservice.booking.service;

import nucleusteq.eventservice.booking.dto.BookingRequestDTO;
import nucleusteq.eventservice.booking.entity.Booking;
import nucleusteq.eventservice.booking.repository.BookingRepository;
import nucleusteq.eventservice.entity.Event;
import nucleusteq.eventservice.exception.BadRequestException;
import nucleusteq.eventservice.exception.ResourceNotFoundException;
import nucleusteq.eventservice.exception.UnauthorizedException;
import nucleusteq.eventservice.repository.EventRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class BookingService {

    private final BookingRepository bookingRepository;
    private final EventRepository eventRepository;

    public BookingService(BookingRepository bookingRepository, EventRepository eventRepository) {
        this.bookingRepository = bookingRepository;
        this.eventRepository = eventRepository;
    }

    @Transactional
    public String bookTickets(BookingRequestDTO requestDTO, String customerEmail) {
        Event event = eventRepository.findById(requestDTO.getEventId())
                .orElseThrow(() -> new ResourceNotFoundException("Event not found"));

        if (event.getAvailableSeats() < requestDTO.getNumberOfTickets()) {
            throw new BadRequestException("Not enough seats available");
        }

        event.setAvailableSeats(event.getAvailableSeats() - requestDTO.getNumberOfTickets());
        eventRepository.save(event);

        Booking booking = Booking.builder()
                .eventId(requestDTO.getEventId())
                .customerEmail(customerEmail)
                .numberOfTickets(requestDTO.getNumberOfTickets())
                .bookingStatus("BOOKED")
                .bookingTime(LocalDateTime.now())
                .build();

        bookingRepository.save(booking);
        return "Tickets Booked Successfully";
    }

    public List<Booking> getMyBookings(String customerEmail) {
        return bookingRepository.findByCustomerEmail(customerEmail);
    }

    @Transactional
    public String cancelBooking(Long bookingId, String customerEmail) {
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found"));

        if (!booking.getCustomerEmail().equals(customerEmail)) {
            throw new UnauthorizedException("You are not authorized to cancel this booking");
        }

        if (booking.getBookingStatus().equals("CANCELLED")) {
            throw new BadRequestException("Booking already cancelled");
        }

        Event event = eventRepository.findById(booking.getEventId())
                .orElseThrow(() -> new ResourceNotFoundException("Event not found"));

        event.setAvailableSeats(event.getAvailableSeats() + booking.getNumberOfTickets());
        eventRepository.save(event);

        booking.setBookingStatus("CANCELLED");
        bookingRepository.save(booking);
        return "Booking Cancelled Successfully";
    }
}