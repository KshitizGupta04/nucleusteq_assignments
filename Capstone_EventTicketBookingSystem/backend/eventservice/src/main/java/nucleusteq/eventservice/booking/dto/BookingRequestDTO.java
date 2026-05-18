package nucleusteq.eventservice.booking.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class BookingRequestDTO {

    @NotNull(message = "Event ID is required")
    private Long eventId;

    @Min(value = 1, message = "At least 1 ticket must be booked")
    private int numberOfTickets;
}