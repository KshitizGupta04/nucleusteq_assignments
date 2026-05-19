package nucleusteq.eventservice.booking.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "bookings")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Booking {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long eventId;

    @Column(nullable = false)
    private String customerEmail;

    @Column(nullable = false)
    private int numberOfTickets;

    @Column(nullable = false)
    private String bookingStatus;

    private LocalDateTime bookingTime;
}