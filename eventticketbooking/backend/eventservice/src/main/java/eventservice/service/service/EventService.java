package eventservice.service.service;

import com.cloudinary.Cloudinary;
import com.cloudinary.utils.ObjectUtils;
import eventservice.service.booking.repository.BookingRepository;
import eventservice.service.entity.Event;
import eventservice.service.exception.BadRequestException;
import eventservice.service.exception.ResourceNotFoundException;
import eventservice.service.repository.EventRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;
import java.util.Map;

@Service
public class EventService {

    private final EventRepository eventRepository;

    private final Cloudinary cloudinary;

    private final BookingRepository bookingRepository;

    public EventService(

            EventRepository eventRepository,

            Cloudinary cloudinary,

            BookingRepository bookingRepository
    ) {

        this.eventRepository = eventRepository;

        this.cloudinary = cloudinary;

        this.bookingRepository = bookingRepository;
    }

    // CREATE EVENT
    public String createEvent(

            String title,

            String description,

            String location,

            String date,

            String time,

            Double price,

            Integer availableSeats,

            MultipartFile image,

            String organizerEmail
    ) {

        try {

            LocalDateTime eventDateTime =
                    LocalDateTime.of(
                            LocalDate.parse(date),
                            LocalTime.parse(time)
                    );

            if (eventDateTime.isBefore(
                    LocalDateTime.now()
            )) {

                throw new BadRequestException(
                        "Event must be scheduled in future"
                );
            }

            if (price <= 0) {

                throw new BadRequestException(
                        "Price must be greater than 0"
                );
            }

            if (availableSeats < 1) {

                throw new BadRequestException(
                        "Available seats must be at least 1"
                );
            }

            Map uploadResult =
                    cloudinary.uploader().upload(

                            image.getBytes(),

                            ObjectUtils.emptyMap()
                    );

            String imageUrl =
                    uploadResult.get("secure_url").toString();

            Event event = Event.builder()

                    .title(title)

                    .description(description)

                    .location(location)

                    .date(date)

                    .time(time)

                    .price(price)

                    .availableSeats(availableSeats)

                    .imageUrl(imageUrl)

                    .organizerEmail(organizerEmail)

                    .build();

            eventRepository.save(event);

            return "Event Created Successfully";

        } catch (BadRequestException e) {

            throw e;

        } catch (Exception e) {

            throw new RuntimeException(
                    e.getMessage()
            );
        }
    }

    // GET ALL EVENTS
    public List<Event> getAllEvents() {

        LocalDate today =
                LocalDate.now();

        LocalTime currentTime =
                LocalTime.now();

        return eventRepository.findAll()

                .stream()

                .filter(event -> {

                    LocalDate eventDate =
                            LocalDate.parse(
                                    event.getDate()
                            );

                    LocalTime eventTime =
                            LocalTime.parse(
                                    event.getTime()
                            );

                    if (eventDate.isAfter(today)) {

                        return true;
                    }

                    return

                            eventDate.isEqual(today)

                                    &&

                                    eventTime.isAfter(currentTime);
                })

                .toList();
    }

    // GET MY EVENTS
    public List<Event> getMyEvents(
            String organizerEmail
    ) {

        LocalDate today =
                LocalDate.now();

        LocalTime currentTime =
                LocalTime.now();

        return eventRepository

                .findByOrganizerEmail(
                        organizerEmail
                )

                .stream()

                .filter(event -> {

                    LocalDate eventDate =
                            LocalDate.parse(
                                    event.getDate()
                            );

                    LocalTime eventTime =
                            LocalTime.parse(
                                    event.getTime()
                            );

                    if (eventDate.isAfter(today)) {

                        return true;
                    }

                    return

                            eventDate.isEqual(today)

                                    &&

                                    eventTime.isAfter(currentTime);
                })

                .toList();
    }

    // GET EVENT BY ID
    public Event getEventById(Long id) {

        return eventRepository.findById(id)

                .orElseThrow(() ->

                        new ResourceNotFoundException(
                                "Event not found"
                        )
                );
    }

    // UPDATE EVENT
    public String updateEvent(

            Long id,

            String title,

            String description,

            String location,

            String date,

            String time,

            Double price,

            Integer availableSeats,

            MultipartFile image,

            String organizerEmail
    ) {

        Event event = eventRepository.findById(id)

                .orElseThrow(() ->

                        new ResourceNotFoundException(
                                "Event not found"
                        )
                );

        if (!event.getOrganizerEmail()
                .equals(organizerEmail)) {

            throw new BadRequestException(
                    "You cannot update another organizer's event"
            );
        }

        LocalDateTime existingEventTime =
                LocalDateTime.of(

                        LocalDate.parse(event.getDate()),

                        LocalTime.parse(event.getTime())
                );

        if (LocalDateTime.now().isAfter(
                existingEventTime.minusHours(4)
        )) {

            throw new BadRequestException(
                    "Event cannot be updated in last 4 hours"
            );
        }

        LocalDateTime newEventDateTime =
                LocalDateTime.of(
                        LocalDate.parse(date),
                        LocalTime.parse(time)
                );

        if (newEventDateTime.isBefore(
                LocalDateTime.now()
        )) {

            throw new BadRequestException(
                    "Event must be scheduled in future"
            );
        }

        if (price <= 0) {

            throw new BadRequestException(
                    "Price must be greater than 0"
            );
        }

        if (availableSeats < 1) {

            throw new BadRequestException(
                    "Available seats must be at least 1"
            );
        }

        // VALIDATE BOOKED TICKETS
        int bookedTickets =

                bookingRepository
                        .findByEventId(event.getId())
                        .stream()

                        .filter(booking ->

                                booking
                                        .getBookingStatus()
                                        .equals("BOOKED")
                        )

                        .mapToInt(booking ->

                                booking.getNumberOfTickets()
                        )

                        .sum();

        if (availableSeats < bookedTickets) {

            throw new BadRequestException(

                    "Seats cannot be less than already booked tickets (" +

                            bookedTickets +

                            ")"
            );
        }


        event.setTitle(title);

        event.setDescription(description);

        event.setLocation(location);

        event.setDate(date);

        event.setTime(time);

        event.setPrice(price);

        event.setAvailableSeats(availableSeats);

        try {

            if (image != null && !image.isEmpty()) {

                Map uploadResult =
                        cloudinary.uploader().upload(

                                image.getBytes(),

                                ObjectUtils.emptyMap()
                        );

                event.setImageUrl(

                        uploadResult.get("secure_url")
                                .toString()
                );
            }

        } catch (Exception e) {

            throw new RuntimeException(
                    e.getMessage()
            );
        }

        eventRepository.save(event);

        return "Event Updated Successfully";
    }

    // DELETE EVENT
    @Transactional
    public String deleteEvent(

            Long id,

            String organizerEmail
    ) {

        Event event = eventRepository.findById(id)

                .orElseThrow(() ->

                        new ResourceNotFoundException(
                                "Event not found"
                        )
                );

        if (!event.getOrganizerEmail()
                .equals(organizerEmail)) {

            throw new BadRequestException(
                    "You cannot delete another organizer's event"
            );
        }

        LocalDateTime eventDateTime =
                LocalDateTime.of(

                        LocalDate.parse(event.getDate()),

                        LocalTime.parse(event.getTime())
                );

        if (LocalDateTime.now().isAfter(
                eventDateTime.minusHours(4)
        )) {

            throw new BadRequestException(
                    "Event cannot be deleted in last 4 hours"
            );
        }

        eventRepository.delete(event);

        return "Event Deleted Successfully";
    }
}