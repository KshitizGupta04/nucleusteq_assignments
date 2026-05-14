package NucleusTeq.Capstone_EventTIcketBookingSystem.service;

import NucleusTeq.Capstone_EventTIcketBookingSystem.dto.LoginRequestDTO;
import NucleusTeq.Capstone_EventTIcketBookingSystem.dto.LoginResponseDTO;
import NucleusTeq.Capstone_EventTIcketBookingSystem.dto.RequestRegisterDTO;

import NucleusTeq.Capstone_EventTIcketBookingSystem.entity.User;

import NucleusTeq.Capstone_EventTIcketBookingSystem.repository.UserRepository;

import NucleusTeq.Capstone_EventTIcketBookingSystem.security.JwtUtil;

import org.springframework.security.crypto.password.PasswordEncoder;

import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final UserRepository userRepository;

    private final PasswordEncoder passwordEncoder;

    private final JwtUtil jwtUtil;

    public AuthService(
            UserRepository userRepository,
            PasswordEncoder passwordEncoder,
            JwtUtil jwtUtil
    ) {

        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtUtil = jwtUtil;
    }

    public String registerUser(
            RequestRegisterDTO requestDTO
    ) {

        User user = new User();

        user.setEmail(requestDTO.getEmail());

        user.setName(requestDTO.getName());

        user.setPassword(
                passwordEncoder.encode(
                        requestDTO.getPassword()
                )
        );

        user.setPhone(requestDTO.getPhone());

        user.setRole(requestDTO.getRole());

        userRepository.save(user);

        return "User registered successfully";
    }

    public LoginResponseDTO loginUser(
            LoginRequestDTO loginRequestDTO
    ) {

        User user = userRepository
                .findByEmail(loginRequestDTO.getEmail())
                .orElseThrow(
                        () -> new RuntimeException("User not found")
                );

        boolean isPasswordCorrect =
                passwordEncoder.matches(
                        loginRequestDTO.getPassword(),
                        user.getPassword()
                );

        if (!isPasswordCorrect) {

            throw new RuntimeException(
                    "Invalid Password"
            );
        }

        String token =
                jwtUtil.generateToken(user.getEmail());

        return new LoginResponseDTO(token);
    }
}