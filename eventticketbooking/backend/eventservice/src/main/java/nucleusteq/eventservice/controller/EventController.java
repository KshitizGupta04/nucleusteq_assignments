package nucleusteq.eventservice.controller;

import nucleusteq.eventservice.dto.EventRequestDTO;
import nucleusteq.eventservice.entity.Event;
import nucleusteq.eventservice.service.EventService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/api/v1/events")
public class EventController {

    private final EventService eventService;

    public EventController(EventService eventService) {
        this.eventService = eventService;
    }

    @PreAuthorize("hasRole('ORGANISER')")
    @PostMapping
    public ResponseEntity<String> createEvent(@Valid @RequestBody EventRequestDTO requestDTO, Authentication authentication) {
        return ResponseEntity.ok(eventService.createEvent(requestDTO, authentication.getName()));
    }

    @GetMapping
    public ResponseEntity<List<Event>> getAllEvents() {
        return ResponseEntity.ok(eventService.getAllEvents());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Event> getEventById(@PathVariable Long id) {
        return ResponseEntity.ok(eventService.getEventById(id));
    }

    @PreAuthorize("hasRole('ORGANISER')")
    @PutMapping("/{id}")
    public ResponseEntity<String> updateEvent(@PathVariable Long id, @Valid @RequestBody EventRequestDTO requestDTO) {
        return ResponseEntity.ok(eventService.updateEvent(id, requestDTO));
    }

    @PreAuthorize("hasRole('ORGANISER')")
    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteEvent(@PathVariable Long id) {
        return ResponseEntity.ok(eventService.deleteEvent(id));
    }
}