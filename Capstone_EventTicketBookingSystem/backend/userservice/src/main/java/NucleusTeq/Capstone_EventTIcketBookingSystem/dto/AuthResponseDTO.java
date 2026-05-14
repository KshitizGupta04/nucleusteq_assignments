package NucleusTeq.Capstone_EventTIcketBookingSystem.dto;
import NucleusTeq.Capstone_EventTIcketBookingSystem.entity.Role;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class AuthResponseDTO {
    private String token;
    private String message;
}
