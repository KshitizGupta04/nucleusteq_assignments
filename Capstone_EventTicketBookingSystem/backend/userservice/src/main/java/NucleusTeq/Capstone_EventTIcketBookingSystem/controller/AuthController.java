package NucleusTeq.Capstone_EventTIcketBookingSystem.controller;

import NucleusTeq.Capstone_EventTIcketBookingSystem.dto.LoginRequestDTO;
import NucleusTeq.Capstone_EventTIcketBookingSystem.dto.LoginResponseDTO;
import NucleusTeq.Capstone_EventTIcketBookingSystem.dto.RequestRegisterDTO;

import NucleusTeq.Capstone_EventTIcketBookingSystem.service.AuthService;

import jakarta.validation.Valid;

import org.springframework.web.bind.annotation.*;

@CrossOrigin(origins = "*")
@RestController

@RequestMapping("/auth")

public class AuthController {

    private final AuthService authService;

    public AuthController(
            AuthService authService
    ) {

        this.authService = authService;
    }

    @PostMapping("/register")

    public String registerUser(

            @Valid @RequestBody
            RequestRegisterDTO requestDTO
    ) {

        return authService.registerUser(
                requestDTO
        );
    }

    @PostMapping("/login")

    public LoginResponseDTO loginUser(

            @Valid @RequestBody
            LoginRequestDTO loginRequestDTO
    ) {

        return authService.loginUser(
                loginRequestDTO
        );
    }
}