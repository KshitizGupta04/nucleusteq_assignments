package eventservice.service.booking.repository;

import eventservice.service.booking.entity.Booking;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface BookingRepository extends JpaRepository<Booking, Long> {

    List<Booking> findByCustomerEmail(String customerEmail);

    List<Booking> findByEventId(Long eventId);
}