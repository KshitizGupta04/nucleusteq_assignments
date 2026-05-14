package NucleusTeq.Capstone_EventTIcketBookingSystem.dto;
import NucleusTeq.Capstone_EventTIcketBookingSystem.entity.Role;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class RequestRegisterDTO {
    private String name;
    private String email;
    private String password;
    private String phone;
    private Role role;
}
