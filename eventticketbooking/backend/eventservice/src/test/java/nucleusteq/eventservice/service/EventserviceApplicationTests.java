package nucleusteq.eventservice.service;

import nucleusteq.eventservice.dto.EventRequestDTO;

import nucleusteq.eventservice.entity.Event;

import nucleusteq.eventservice.exception.ResourceNotFoundException;

import nucleusteq.eventservice.repository.EventRepository;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class EventServiceTest {

	@Mock
	private EventRepository eventRepository;

	@InjectMocks
	private EventService eventService;

	@BeforeEach
	void setup() {

		MockitoAnnotations.openMocks(this);
	}

	// CREATE EVENT TEST
	@Test
	void createEventSuccess() {

		EventRequestDTO dto =
				new EventRequestDTO(

						"Music Concert",

						"Live concert event",

						"Delhi",

						"2025-12-20",

						"7:00 PM",

						999.0,

						100
				);

		String response =
				eventService.createEvent(
						dto,
						"admin@gmail.com"
				);

		assertEquals(

				"Event Created Successfully",

				response
		);

		verify(eventRepository, times(1))
				.save(any(Event.class));
	}

	// GET EVENT BY ID TEST
	@Test
	void getEventByIdSuccess() {

		Event event = Event.builder()

				.id(1L)

				.title("Concert")

				.build();

		when(eventRepository.findById(1L))
				.thenReturn(Optional.of(event));

		Event response =
				eventService.getEventById(1L);

		assertNotNull(response);

		assertEquals(

				"Concert",

				response.getTitle()
		);
	}

	// EVENT NOT FOUND TEST
	@Test
	void getEventByIdNotFound() {

		when(eventRepository.findById(1L))
				.thenReturn(Optional.empty());

		assertThrows(

				ResourceNotFoundException.class,

				() -> eventService.getEventById(1L)
		);
	}

	// DELETE EVENT TEST
	@Test
	void deleteEventSuccess() {

		Event event = Event.builder()

				.id(1L)

				.title("Concert")

				.build();

		when(eventRepository.findById(1L))
				.thenReturn(Optional.of(event));

		String response =
				eventService.deleteEvent(1L);

		assertEquals(

				"Event Deleted Successfully",

				response
		);

		verify(eventRepository, times(1))
				.delete(event);
	}
}