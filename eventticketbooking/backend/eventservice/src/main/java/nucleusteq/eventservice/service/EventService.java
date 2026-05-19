package nucleusteq.eventservice.service;

import nucleusteq.eventservice.dto.EventRequestDTO;
import nucleusteq.eventservice.entity.Event;
import nucleusteq.eventservice.exception.ResourceNotFoundException;
import nucleusteq.eventservice.repository.EventRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class EventService {

    private final EventRepository eventRepository;

    public EventService(EventRepository eventRepository) {
        this.eventRepository = eventRepository;
    }

    public String createEvent(EventRequestDTO requestDTO, String organizerEmail) {
        Event event = Event.builder()
                .title(requestDTO.getTitle())
                .description(requestDTO.getDescription())
                .location(requestDTO.getLocation())
                .date(requestDTO.getDate())
                .time(requestDTO.getTime())
                .price(requestDTO.getPrice())
                .availableSeats(requestDTO.getAvailableSeats())
                .organizerEmail(organizerEmail)
                .build();

        eventRepository.save(event);
        return "Event Created Successfully";
    }

    public List<Event> getAllEvents() {
        return eventRepository.findAll();
    }

    public Event getEventById(Long id) {
        return eventRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Event not found"));
    }

    public String updateEvent(Long id, EventRequestDTO requestDTO) {
        Event event = eventRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Event not found"));

        event.setTitle(requestDTO.getTitle());
        event.setDescription(requestDTO.getDescription());
        event.setLocation(requestDTO.getLocation());
        event.setDate(requestDTO.getDate());
        event.setTime(requestDTO.getTime());
        event.setPrice(requestDTO.getPrice());
        event.setAvailableSeats(requestDTO.getAvailableSeats());

        eventRepository.save(event);
        return "Event Updated Successfully";
    }

    public String deleteEvent(Long id) {
        Event event = eventRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Event not found"));

        eventRepository.delete(event);
        return "Event Deleted Successfully";
    }
}