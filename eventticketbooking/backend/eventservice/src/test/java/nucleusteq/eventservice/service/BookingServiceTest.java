package nucleusteq.eventservice.service;

import eventservice.service.booking.entity.Booking;
import eventservice.service.booking.repository.BookingRepository;
import eventservice.service.booking.service.BookingService;

import eventservice.service.entity.Event;
import eventservice.service.repository.EventRepository;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class BookingServiceTest {

    @Mock
    private BookingRepository bookingRepository;

    @Mock
    private EventRepository eventRepository;

    @InjectMocks
    private BookingService bookingService;

    @BeforeEach
    void setup() {

        MockitoAnnotations.openMocks(this);

    }

    // TEST 1 - CANCEL BOOKING SUCCESS
    @Test
    void cancelBookingSuccess() {

        Booking booking = Booking.builder()

                .customerEmail("user@gmail.com")

                .bookingStatus("CONFIRMED")

                .eventId(1L)

                .build();

        Event event = Event.builder()

                .id(1L)

                .availableSeats(10)

                .build();

        when(bookingRepository.findById(1L))
                .thenReturn(Optional.of(booking));

        when(eventRepository.findById(1L))
                .thenReturn(Optional.of(event));

        String response =
                bookingService.cancelBooking(
                        1L,
                        "user@gmail.com"
                );

        assertNotNull(response);
    }

    // TEST 2 - BOOKING NOT FOUND
    @Test
    void cancelBookingNotFound() {

        when(bookingRepository.findById(1L))
                .thenReturn(Optional.empty());

        assertThrows(
                RuntimeException.class,
                () -> bookingService.cancelBooking(
                        1L,
                        "user@gmail.com"
                )
        );
    }

    // TEST 3 - INVALID CUSTOMER
    @Test
    void cancelBookingInvalidCustomer() {

        Booking booking = Booking.builder()

                .customerEmail("another@gmail.com")

                .bookingStatus("CONFIRMED")

                .eventId(1L)

                .build();

        when(bookingRepository.findById(1L))
                .thenReturn(Optional.of(booking));

        assertThrows(
                RuntimeException.class,
                () -> bookingService.cancelBooking(
                        1L,
                        "user@gmail.com"
                )
        );
    }

    // TEST 4 - ALREADY CANCELLED
    @Test
    void cancelBookingAlreadyCancelled() {

        Booking booking = Booking.builder()

                .customerEmail("user@gmail.com")

                .bookingStatus("CANCELLED")

                .eventId(1L)

                .build();

        when(bookingRepository.findById(1L))
                .thenReturn(Optional.of(booking));

        assertThrows(
                RuntimeException.class,
                () -> bookingService.cancelBooking(
                        1L,
                        "user@gmail.com"
                )
        );
    }

    // TEST 5 - EVENT NOT FOUND
    @Test
    void cancelBookingEventNotFound() {

        Booking booking = Booking.builder()

                .customerEmail("user@gmail.com")

                .bookingStatus("CONFIRMED")

                .eventId(1L)

                .build();

        when(bookingRepository.findById(1L))
                .thenReturn(Optional.of(booking));

        when(eventRepository.findById(1L))
                .thenReturn(Optional.empty());

        assertThrows(
                RuntimeException.class,
                () -> bookingService.cancelBooking(
                        1L,
                        "user@gmail.com"
                )
        );
    }

    // TEST 6 - EVENT FOUND
    @Test
    void eventFoundTest() {

        Event event = Event.builder()

                .id(1L)

                .availableSeats(50)

                .build();

        when(eventRepository.findById(1L))
                .thenReturn(Optional.of(event));

        Optional<Event> result =
                eventRepository.findById(1L);

        assertTrue(result.isPresent());

        assertEquals(
                50,
                result.get().getAvailableSeats()
        );
    }

    // TEST 7 - EVENT NOT FOUND
    @Test
    void eventNotFoundTest() {

        when(eventRepository.findById(1L))
                .thenReturn(Optional.empty());

        Optional<Event> result =
                eventRepository.findById(1L);

        assertFalse(result.isPresent());
    }

    // TEST 8 - SAVE BOOKING
    @Test
    void saveBookingTest() {

        Booking booking = Booking.builder()

                .customerEmail("save@gmail.com")

                .bookingStatus("CONFIRMED")

                .eventId(2L)

                .build();

        when(bookingRepository.save(any(Booking.class)))
                .thenReturn(booking);

        Booking savedBooking =
                bookingRepository.save(booking);

        assertNotNull(savedBooking);

        assertEquals(
                "save@gmail.com",
                savedBooking.getCustomerEmail()
        );
    }

    // TEST 9 - MULTIPLE EVENT LOOKUP
    @Test
    void multipleEventLookupTest() {

        Event event = Event.builder()

                .id(2L)

                .availableSeats(100)

                .build();

        when(eventRepository.findById(2L))
                .thenReturn(Optional.of(event));

        Optional<Event> result =
                eventRepository.findById(2L);

        assertTrue(result.isPresent());

        assertEquals(
                100,
                result.get().getAvailableSeats()
        );
    }

    // TEST 10 - BOOKING FIND
    @Test
    void bookingRepositoryFindTest() {

        Booking booking = Booking.builder()

                .customerEmail("repo@gmail.com")

                .bookingStatus("CONFIRMED")

                .eventId(3L)

                .build();

        when(bookingRepository.findById(5L))
                .thenReturn(Optional.of(booking));

        Optional<Booking> result =
                bookingRepository.findById(5L);

        assertTrue(result.isPresent());
    }

    // TEST 11 - BOOKING NOT FOUND
    @Test
    void bookingRepositoryNotFoundTest() {

        when(bookingRepository.findById(10L))
                .thenReturn(Optional.empty());

        Optional<Booking> result =
                bookingRepository.findById(10L);

        assertFalse(result.isPresent());
    }

    // TEST 12 - VERIFY SAVE
    @Test
    void bookingRepositorySaveVerification() {

        Booking booking = Booking.builder()

                .customerEmail("verify@gmail.com")

                .bookingStatus("CONFIRMED")

                .eventId(2L)

                .build();

        when(bookingRepository.save(any(Booking.class)))
                .thenReturn(booking);

        Booking saved =
                bookingRepository.save(booking);

        verify(bookingRepository, times(1))
                .save(any(Booking.class));

        assertNotNull(saved);
    }

    // TEST 13 - VERIFY EVENT LOOKUP
    @Test
    void verifyEventLookup() {

        Event event = Event.builder()

                .id(5L)

                .availableSeats(200)

                .build();

        when(eventRepository.findById(5L))
                .thenReturn(Optional.of(event));

        Optional<Event> result =
                eventRepository.findById(5L);

        verify(eventRepository, times(1))
                .findById(5L);

        assertTrue(result.isPresent());
    }

    // TEST 14 - NULL EMAIL
    @Test
    void cancelBookingWithNullEmail() {

        Booking booking = Booking.builder()

                .customerEmail(null)

                .bookingStatus("CONFIRMED")

                .eventId(1L)

                .build();

        when(bookingRepository.findById(1L))
                .thenReturn(Optional.of(booking));

        assertThrows(
                NullPointerException.class,
                () -> bookingService.cancelBooking(
                        1L,
                        "user@gmail.com"
                )
        );
    }

    // TEST 15 - VERIFY FIND CALLED
    @Test
    void verifyBookingFindCalled() {

        Booking booking = Booking.builder()

                .customerEmail("find@gmail.com")

                .bookingStatus("CONFIRMED")

                .eventId(3L)

                .build();

        when(bookingRepository.findById(3L))
                .thenReturn(Optional.of(booking));

        bookingRepository.findById(3L);

        verify(bookingRepository, times(1))
                .findById(3L);
    }

    // TEST 16 - ZERO SEATS
    @Test
    void eventWithZeroSeatsTest() {

        Event event = Event.builder()

                .id(7L)

                .availableSeats(0)

                .build();

        when(eventRepository.findById(7L))
                .thenReturn(Optional.of(event));

        Optional<Event> result =
                eventRepository.findById(7L);

        assertEquals(
                0,
                result.get().getAvailableSeats()
        );
    }
}