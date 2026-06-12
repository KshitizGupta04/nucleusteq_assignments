package userservice.controller;

import userservice.dto.LoginRequestDTO;
import userservice.dto.LoginResponseDTO;
import userservice.dto.RequestRegisterDTO;
import userservice.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/api/v1/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    public ResponseEntity<String> registerUser(@Valid @RequestBody RequestRegisterDTO requestDTO) {
        return ResponseEntity.ok(authService.registerUser(requestDTO));
    }

    @PostMapping("/login")
    public ResponseEntity<LoginResponseDTO> loginUser(@Valid @RequestBody LoginRequestDTO loginRequestDTO) {
        return ResponseEntity.ok(authService.loginUser(loginRequestDTO));
    }
}