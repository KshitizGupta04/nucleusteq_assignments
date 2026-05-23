package eventservice.service.repository;

import eventservice.service.entity.Event;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface EventRepository
        extends JpaRepository<Event, Long> {

    // ORGANIZER EVENTS
    List<Event> findByOrganizerEmail(
            String organizerEmail
    );
}