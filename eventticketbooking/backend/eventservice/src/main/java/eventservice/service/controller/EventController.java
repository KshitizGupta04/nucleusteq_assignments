package eventservice.service.controller;

import eventservice.service.entity.Event;
import eventservice.service.service.EventService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@CrossOrigin(origins = "*")

@RestController

@RequestMapping("/api/v1/events")
public class EventController {

    private final EventService eventService;

    public EventController(
            EventService eventService
    ) {

        this.eventService = eventService;
    }

    // CREATE EVENT
    @PreAuthorize("hasRole('ORGANISER')")

    @PostMapping(
            consumes = "multipart/form-data"
    )

    public ResponseEntity<String> createEvent(

            @RequestParam("title")
            String title,

            @RequestParam("description")
            String description,

            @RequestParam("location")
            String location,

            @RequestParam("date")
            String date,

            @RequestParam("time")
            String time,

            @RequestParam("price")
            Double price,

            @RequestParam("availableSeats")
            Integer availableSeats,

            @RequestParam("image")
            MultipartFile image,

            Authentication authentication
    ) {

        return ResponseEntity.ok(

                eventService.createEvent(

                        title,

                        description,

                        location,

                        date,

                        time,

                        price,

                        availableSeats,

                        image,

                        authentication.getName()
                )
        );
    }


    // ============================
    // GET ALL EVENTS
    // ============================

    @GetMapping
    public ResponseEntity<List<Event>> getAllEvents() {

        return ResponseEntity.ok(
                eventService.getAllEvents()
        );
    }


    // GET MY EVENTS
    @PreAuthorize("hasRole('ORGANISER')")

    @GetMapping("/my-events")
    public ResponseEntity<List<Event>> getMyEvents(
            Authentication authentication
    ) {

        return ResponseEntity.ok(

                eventService.getMyEvents(
                        authentication.getName()
                )
        );
    }

    // GET EVENT BY ID
    @GetMapping("/{id}")
    public ResponseEntity<Event> getEventById(
            @PathVariable Long id
    ) {

        return ResponseEntity.ok(
                eventService.getEventById(id)
        );
    }

    // UPDATE EVENT
    @PreAuthorize("hasRole('ORGANISER')")

    @PutMapping(
            value = "/{id}",
            consumes = "multipart/form-data"
    )

    public ResponseEntity<String> updateEvent(

            @PathVariable Long id,

            @RequestParam("title")
            String title,

            @RequestParam("description")
            String description,

            @RequestParam("location")
            String location,

            @RequestParam("date")
            String date,

            @RequestParam("time")
            String time,

            @RequestParam("price")
            Double price,

            @RequestParam("availableSeats")
            Integer availableSeats,

            @RequestParam(
                    value = "image",
                    required = false
            )
            MultipartFile image,

            Authentication authentication
    ) {

        return ResponseEntity.ok(

                eventService.updateEvent(

                        id,

                        title,

                        description,

                        location,

                        date,

                        time,

                        price,

                        availableSeats,

                        image,

                        authentication.getName()
                )
        );
    }

    // DELETE EVENT
    @PreAuthorize("hasRole('ORGANISER')")

    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteEvent(

            @PathVariable Long id,

            Authentication authentication
    ) {

        return ResponseEntity.ok(

                eventService.deleteEvent(

                        id,

                        authentication.getName()
                )
        );
    }
}