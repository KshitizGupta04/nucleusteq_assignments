package eventservice.service.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "events")

@Getter
@Setter

@NoArgsConstructor
@AllArgsConstructor

@Builder

public class Event {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)

    private Long id;

    @Column(nullable = false)

    private String title;

    private String description;

    @Column(nullable = false)

    private String location;

    @Column(nullable = false)

    private String date;

    @Column(nullable = false)

    private String time;

    @Column(nullable = false)

    private Double price;

    @Column(nullable = false)

    private Integer availableSeats;

    @Column(nullable = false)

    private String organizerEmail;

    @Column(name = "image_url")

    private String imageUrl;
}