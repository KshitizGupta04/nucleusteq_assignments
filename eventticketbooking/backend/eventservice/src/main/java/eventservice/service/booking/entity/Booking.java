package eventservice.service.booking.entity;

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

    // EVENT INFO
    @Column(nullable = false)

    private Long eventId;


    @Column(nullable = false)

    private String customerEmail;


    @Column(nullable = false)

    private Integer numberOfTickets;


    @Column(nullable = false)

    private String bookingStatus;


    @Column(nullable = false)

    private LocalDateTime bookingTime;


    // EXTRA EVENT DETAILS
    @Transient
    private String eventTitle;

    @Transient
    private String eventDate;

    @Transient
    private String eventTime;

    @Transient
    private String eventLocation;
}