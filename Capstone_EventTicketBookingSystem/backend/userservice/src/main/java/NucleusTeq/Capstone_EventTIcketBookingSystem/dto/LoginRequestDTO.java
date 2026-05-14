package NucleusTeq.Capstone_EventTIcketBookingSystem.dto;
import NucleusTeq.Capstone_EventTIcketBookingSystem.entity.Role;
import lombok.*;


@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class LoginRequestDTO {
    private String email;
    private String password;
}
