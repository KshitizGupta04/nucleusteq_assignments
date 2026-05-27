package eventservice.service.booking.service;

import eventservice.service.booking.dto.BookingRequestDTO;
import eventservice.service.booking.entity.Booking;
import eventservice.service.booking.repository.BookingRepository;
import eventservice.service.entity.Event;
import eventservice.service.exception.BadRequestException;
import eventservice.service.exception.ResourceNotFoundException;
import eventservice.service.exception.UnauthorizedException;
import eventservice.service.repository.EventRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;

@Service
public class BookingService {

    private final BookingRepository bookingRepository;

    private final EventRepository eventRepository;

    public BookingService(

            BookingRepository bookingRepository,

            EventRepository eventRepository
    ) {

        this.bookingRepository = bookingRepository;

        this.eventRepository = eventRepository;
    }

    // BOOK TICKETS
    @Transactional
    public String bookTickets(

            BookingRequestDTO requestDTO,

            String customerEmail
    ) {

        Event event = eventRepository.findById(
                        requestDTO.getEventId()
                )

                .orElseThrow(() ->

                        new ResourceNotFoundException(
                                "Event not found"
                        )
                );

        // EVENT TIME VALIDATION
        LocalDateTime eventDateTime =

                LocalDateTime.of(

                        LocalDate.parse(
                                event.getDate()
                        ),

                        LocalTime.parse(
                                event.getTime()
                        )
                );

        if (

                eventDateTime.isBefore(
                        LocalDateTime.now()
                )
        ) {

            throw new BadRequestException(
                    "Cannot book past events"
            );
        }

        // TICKET VALIDATION
        if (

                requestDTO.getNumberOfTickets() < 1
        ) {

            throw new BadRequestException(
                    "Minimum 1 ticket required"
            );
        }

        if (

                requestDTO.getNumberOfTickets() > 10
        ) {

            throw new BadRequestException(
                    "Maximum 10 tickets allowed per booking"
            );
        }

        if (

                event.getAvailableSeats()

                        <

                        requestDTO.getNumberOfTickets()
        ) {

            throw new BadRequestException(
                    "Not enough seats available"
            );
        }

        // UPDATE SEATS
        event.setAvailableSeats(

                event.getAvailableSeats()

                        -

                        requestDTO.getNumberOfTickets()
        );

        eventRepository.save(event);

        // SAVE BOOKING
        Booking booking = Booking.builder()

                .eventId(
                        requestDTO.getEventId()
                )

                .customerEmail(
                        customerEmail
                )

                .numberOfTickets(
                        requestDTO.getNumberOfTickets()
                )

                .bookingStatus("BOOKED")

                .bookingTime(
                        LocalDateTime.now()
                )

                .build();

        bookingRepository.save(booking);

        return "Tickets Booked Successfully";
    }


    // GET MY BOOKINGS
    public List<Booking> getMyBookings(
            String customerEmail
    ) {

        List<Booking> bookings =

                bookingRepository.findByCustomerEmail(
                        customerEmail
                );

        bookings.forEach(booking -> {

            Event event = eventRepository.findById(
                    booking.getEventId()
            ).orElse(null);

            if (event != null) {

                booking.setEventTitle(
                        event.getTitle()
                );

                booking.setEventDate(
                        event.getDate()
                );

                booking.setEventTime(
                        event.getTime()
                );

                booking.setEventLocation(
                        event.getLocation()
                );
            }
        });

        return bookings;
    }

    // ORGANIZER BOOKINGS
    public List<Booking> getBookingsForOrganizerEvent(

            Long eventId,

            String organizerEmail
    ) {

        Event event = eventRepository.findById(eventId)

                .orElseThrow(() ->

                        new ResourceNotFoundException(
                                "Event not found"
                        )
                );

        if (

                !event.getOrganizerEmail()
                        .equals(organizerEmail)
        ) {

            throw new UnauthorizedException(

                    "You cannot view bookings of another organizer"
            );
        }

        return bookingRepository.findByEventId(
                eventId
        );
    }

    // CANCEL BOOKING
    @Transactional
    public String cancelBooking(

            Long bookingId,

            String customerEmail
    ) {

        Booking booking = bookingRepository.findById(
                        bookingId
                )

                .orElseThrow(() ->

                        new ResourceNotFoundException(
                                "Booking not found"
                        )
                );

        if (

                !booking.getCustomerEmail()
                        .equals(customerEmail)
        ) {

            throw new UnauthorizedException(

                    "You are not authorized to cancel this booking"
            );
        }

        if (

                booking.getBookingStatus()
                        .equals("CANCELLED")
        ) {

            throw new BadRequestException(
                    "Booking already cancelled"
            );
        }

        Event event = eventRepository.findById(
                        booking.getEventId()
                )

                .orElseThrow(() ->

                        new ResourceNotFoundException(
                                "Event not found"
                        )
                );

        // LAST 4 HOURS RESTRICTION
        LocalDateTime eventDateTime =

                LocalDateTime.of(

                        LocalDate.parse(
                                event.getDate()
                        ),

                        LocalTime.parse(
                                event.getTime()
                        )
                );

        if (

                LocalDateTime.now().isAfter(

                        eventDateTime.minusHours(4)
                )
        ) {

            throw new BadRequestException(

                    "Booking cannot be cancelled within last 4 hours of event"
            );
        }

        // RESTORE SEATS
        event.setAvailableSeats(

                event.getAvailableSeats()

                        +

                        booking.getNumberOfTickets()
        );

        eventRepository.save(event);

        // UPDATE STATUS
        booking.setBookingStatus(
                "CANCELLED"
        );

        bookingRepository.save(booking);

        return "Booking Cancelled Successfully";
    }
}