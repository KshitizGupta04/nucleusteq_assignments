package nucleusteq.eventservice.service;

import com.cloudinary.Cloudinary;
import com.cloudinary.Uploader;
import eventservice.service.booking.repository.BookingRepository;
import eventservice.service.entity.Event;
import eventservice.service.exception.BadRequestException;
import eventservice.service.exception.ResourceNotFoundException;
import eventservice.service.repository.EventRepository;
import eventservice.service.service.EventService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.mock.web.MockMultipartFile;

import java.time.LocalDate;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class EventServiceTest {

	@Mock
	private EventRepository eventRepository;

	@Mock
	private Cloudinary cloudinary;

	@Mock
	private Uploader uploader;

	@Mock
	private BookingRepository bookingRepository;

	@InjectMocks
	private EventService eventService;

	@BeforeEach
	void setup() {

		MockitoAnnotations.openMocks(this);
	}


	// =====================================
	// CREATE EVENT TEST
	// =====================================

	@Test
	void createEventSuccess() throws Exception {

		MockMultipartFile image =

				new MockMultipartFile(

						"image",

						"test.jpg",

						"image/jpeg",

						"dummy-image".getBytes()
				);

		Map<String, String> uploadResult =
				new HashMap<>();

		uploadResult.put(
				"secure_url",
				"https://cloudinary.com/test.jpg"
		);

		when(cloudinary.uploader())
				.thenReturn(uploader);

		when(uploader.upload(
				any(byte[].class),
				any(Map.class)
		)).thenReturn(uploadResult);

		String response =

				eventService.createEvent(

						"Music Concert",

						"Live concert event",

						"Delhi",

						"2026-12-20",

						"19:00",

						999.0,

						100,

						image,

						"admin@gmail.com"
				);

		assertEquals(
				"Event Created Successfully",
				response
		);

		verify(eventRepository, times(1))
				.save(any(Event.class));
	}


	// =====================================
	// GET EVENT TEST
	// =====================================

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


	// =====================================
	// EVENT NOT FOUND
	// =====================================

	@Test
	void getEventByIdNotFound() {

		when(eventRepository.findById(1L))
				.thenReturn(Optional.empty());

		assertThrows(

				ResourceNotFoundException.class,

				() -> eventService.getEventById(1L)
		);
	}


	// =====================================
	// UPDATE EVENT SUCCESS
	// =====================================

	@Test
	void updateEventSuccess() {

		Event event = Event.builder()

				.id(1L)

				.title("Old Event")

				.organizerEmail("admin@gmail.com")

				.build();

		when(eventRepository.findById(1L))
				.thenReturn(Optional.of(event));

		String response =

				eventService.updateEvent(

						1L,

						"Updated Event",

						"Updated Desc",

						"Mumbai",

						"2026-12-20",

						"19:00",

						1200.0,

						200,

						null,

						"admin@gmail.com"
				);

		assertEquals(
				"Event Updated Successfully",
				response
		);
	}


	// =====================================
	// UPDATE EVENT UNAUTHORIZED
	// =====================================

	@Test
	void updateEventUnauthorized() {

		Event event = Event.builder()

				.id(1L)

				.organizerEmail("owner@gmail.com")

				.build();

		when(eventRepository.findById(1L))
				.thenReturn(Optional.of(event));

		assertThrows(

				BadRequestException.class,

				() -> eventService.updateEvent(

						1L,

						"Updated Event",

						"Updated Desc",

						"Mumbai",

						"2026-12-20",

						"19:00",

						1200.0,

						200,

						null,

						"other@gmail.com"
				)
		);
	}


	// =====================================
	// DELETE EVENT SUCCESS
	// =====================================

	@Test
	void deleteEventSuccess() {

		Event event = Event.builder()

				.id(1L)

				.title("Concert")

				.organizerEmail("admin@gmail.com")

				.date(LocalDate.now().plusDays(2).toString())

				.time("19:00")

				.build();

		when(eventRepository.findById(1L))
				.thenReturn(Optional.of(event));

		String response =

				eventService.deleteEvent(

						1L,

						"admin@gmail.com"
				);

		assertEquals(
				"Event Deleted Successfully",
				response
		);

		verify(eventRepository, times(1))
				.delete(event);
	}


	// =====================================
	// DELETE EVENT NOT FOUND
	// =====================================

	@Test
	void deleteEventNotFound() {

		when(eventRepository.findById(1L))
				.thenReturn(Optional.empty());

		assertThrows(

				ResourceNotFoundException.class,

				() -> eventService.deleteEvent(

						1L,

						"admin@gmail.com"
				)
		);
	}


	// =====================================
	// DELETE EVENT WITHIN 4 HOURS
	// =====================================

	@Test
	void deleteEventWithin4Hours() {

		Event event = Event.builder()

				.id(1L)

				.organizerEmail("admin@gmail.com")

				.date(LocalDate.now().toString())

				.time("23:59")

				.build();

		when(eventRepository.findById(1L))
				.thenReturn(Optional.of(event));

		assertThrows(

				BadRequestException.class,

				() -> eventService.deleteEvent(

						1L,

						"admin@gmail.com"
				)
		);
	}
}