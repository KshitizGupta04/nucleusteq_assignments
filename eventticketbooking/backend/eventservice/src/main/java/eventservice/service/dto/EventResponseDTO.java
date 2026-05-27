package eventservice.service.dto;

import lombok.*;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EventResponseDTO {

    private Long id;
    private String title;
    private String description;
    private String location;
    private String date;
    private String time;
    private Double price;
    private Integer availableSeats;
    private String organizerEmail;
}