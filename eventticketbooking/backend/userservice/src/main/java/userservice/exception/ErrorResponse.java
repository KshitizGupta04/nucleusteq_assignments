package userservice.exception;

import java.time.LocalDateTime;
import lombok.*;

@Getter
@AllArgsConstructor
public class ErrorResponse {

    private LocalDateTime timestamp;
    private int status;
    private String error;
    private String message;
}