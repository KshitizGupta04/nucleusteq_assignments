package eventservice.service.booking.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.*;

@Getter
@Setter

@NoArgsConstructor
@AllArgsConstructor

public class BookingRequestDTO {

    @NotNull(
            message = "Event ID is required"
    )

    private Long eventId;


    @Min(

            value = 1,

            message = "Minimum 1 ticket required"
    )

    @Max(

            value = 10,

            message = "Maximum 10 tickets allowed"
    )

    private int numberOfTickets;
}