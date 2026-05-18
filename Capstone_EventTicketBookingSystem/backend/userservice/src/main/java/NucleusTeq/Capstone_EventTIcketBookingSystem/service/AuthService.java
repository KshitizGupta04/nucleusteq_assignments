package NucleusTeq.Capstone_EventTIcketBookingSystem.service;

import NucleusTeq.Capstone_EventTIcketBookingSystem.dto.LoginRequestDTO;
import NucleusTeq.Capstone_EventTIcketBookingSystem.dto.LoginResponseDTO;
import NucleusTeq.Capstone_EventTIcketBookingSystem.dto.RequestRegisterDTO;
import NucleusTeq.Capstone_EventTIcketBookingSystem.entity.User;
import NucleusTeq.Capstone_EventTIcketBookingSystem.exception.BadRequestException;
import NucleusTeq.Capstone_EventTIcketBookingSystem.exception.ResourceNotFoundException;
import NucleusTeq.Capstone_EventTIcketBookingSystem.repository.UserRepository;
import NucleusTeq.Capstone_EventTIcketBookingSystem.security.JwtUtil;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;

    public AuthService(UserRepository userRepository, PasswordEncoder passwordEncoder, JwtUtil jwtUtil) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtUtil = jwtUtil;
    }

    public String registerUser(RequestRegisterDTO requestDTO) {
        if (userRepository.existsByEmail(requestDTO.getEmail())) {
            throw new BadRequestException("Email already exists");
        }

        User user = User.builder()
                .name(requestDTO.getName())
                .email(requestDTO.getEmail())
                .password(passwordEncoder.encode(requestDTO.getPassword()))
                .phone(requestDTO.getPhone())
                .role(requestDTO.getRole())
                .build();

        userRepository.save(user);
        return "User registered successfully";
    }

    public LoginResponseDTO loginUser(LoginRequestDTO loginRequestDTO) {
        User user = userRepository.findByEmail(loginRequestDTO.getEmail())
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        if (!passwordEncoder.matches(loginRequestDTO.getPassword(), user.getPassword())) {
            throw new BadRequestException("Invalid password");
        }

        String token = jwtUtil.generateToken(user.getEmail(), user.getRole().name());
        return new LoginResponseDTO(token);
    }
}