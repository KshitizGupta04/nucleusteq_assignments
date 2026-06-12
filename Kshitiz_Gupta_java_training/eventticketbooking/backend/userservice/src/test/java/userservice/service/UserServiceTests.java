package userservice.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import org.springframework.security.crypto.password.PasswordEncoder;

import userservice.dto.LoginRequestDTO;
import userservice.dto.LoginResponseDTO;
import userservice.dto.RequestRegisterDTO;

import userservice.entity.Role;
import userservice.entity.User;

import userservice.exception.BadRequestException;

import userservice.repository.UserRepository;

import userservice.security.JwtUtil;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class AuthServiceTest {

	@Mock
	private UserRepository userRepository;

	@Mock
	private PasswordEncoder passwordEncoder;

	@Mock
	private JwtUtil jwtUtil;

	@InjectMocks
	private AuthService authService;

	@BeforeEach
	void setup() {

		MockitoAnnotations.openMocks(this);
	}

	// REGISTER SUCCESS TEST
	@Test
	void registerUserSuccess() {

		RequestRegisterDTO dto =
				new RequestRegisterDTO(

						"John Doe",

						"john@gmail.com",

						"password123",

						"9999999999",

						Role.CUSTOMER
				);

		when(userRepository.existsByEmail(
				dto.getEmail()
		)).thenReturn(false);

		when(passwordEncoder.encode(
				dto.getPassword()
		)).thenReturn("encodedPassword");

		String response =
				authService.registerUser(dto);

		assertEquals(

				"User registered successfully",

				response
		);

		verify(userRepository, times(1))

				.save(any(User.class));
	}

	// DUPLICATE EMAIL TEST
	@Test
	void registerUserEmailAlreadyExists() {

		RequestRegisterDTO dto =
				new RequestRegisterDTO();

		dto.setEmail(
				"john@gmail.com"
		);

		when(userRepository.existsByEmail(
				dto.getEmail()
		)).thenReturn(true);

		assertThrows(

				BadRequestException.class,

				() -> authService.registerUser(dto)
		);
	}

	// LOGIN SUCCESS TEST
	@Test
	void loginUserSuccess() {

		LoginRequestDTO dto =
				new LoginRequestDTO(

						"john@gmail.com",

						"password123"
				);

		User user = User.builder()

				.email(
						"john@gmail.com"
				)

				.password(
						"encodedPassword"
				)

				.role(
						Role.CUSTOMER
				)

				.build();

		when(userRepository.findByEmail(
				dto.getEmail()
		)).thenReturn(Optional.of(user));

		when(passwordEncoder.matches(

				dto.getPassword(),

				user.getPassword()

		)).thenReturn(true);

		when(jwtUtil.generateToken(

				user.getEmail(),

				user.getRole().name()

		)).thenReturn("jwt-token");

		LoginResponseDTO response =
				authService.loginUser(dto);

		assertNotNull(response);

		assertEquals(

				"jwt-token",

				response.getToken()
		);
	}

	// INVALID PASSWORD TEST
	@Test
	void loginUserInvalidPassword() {

		LoginRequestDTO dto =
				new LoginRequestDTO(

						"john@gmail.com",

						"wrongpassword"
				);

		User user = User.builder()

				.email(
						"john@gmail.com"
				)

				.password(
						"encodedPassword"
				)

				.role(
						Role.CUSTOMER
				)

				.build();

		when(userRepository.findByEmail(
				dto.getEmail()
		)).thenReturn(Optional.of(user));

		when(passwordEncoder.matches(

				dto.getPassword(),

				user.getPassword()

		)).thenReturn(false);

		assertThrows(

				BadRequestException.class,

				() -> authService.loginUser(dto)
		);
	}
}