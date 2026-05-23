package eventservice.service.exception;

import org.springframework.http.HttpStatus;

import org.springframework.http.ResponseEntity;

import org.springframework.security.access.AccessDeniedException;

import org.springframework.web.bind.MethodArgumentNotValidException;

import org.springframework.web.bind.annotation.ExceptionHandler;

import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.LocalDateTime;

import java.util.HashMap;

import java.util.Map;

@RestControllerAdvice

public class GlobalExceptionHandler {

    // RESOURCE NOT FOUND
    @ExceptionHandler(
            ResourceNotFoundException.class
    )

    public ResponseEntity<ErrorResponse>
    handleResourceNotFound(

            ResourceNotFoundException ex
    ) {

        ErrorResponse error =
                new ErrorResponse(

                        LocalDateTime.now(),

                        HttpStatus.NOT_FOUND.value(),

                        "Not Found",

                        ex.getMessage()
                );

        return new ResponseEntity<>(
                error,
                HttpStatus.NOT_FOUND
        );
    }

    // BAD REQUEST
    @ExceptionHandler(
            BadRequestException.class
    )

    public ResponseEntity<ErrorResponse>
    handleBadRequest(

            BadRequestException ex
    ) {

        ErrorResponse error =
                new ErrorResponse(

                        LocalDateTime.now(),

                        HttpStatus.BAD_REQUEST.value(),

                        "Bad Request",

                        ex.getMessage()
                );

        return new ResponseEntity<>(
                error,
                HttpStatus.BAD_REQUEST
        );
    }

    // UNAUTHORIZED
    @ExceptionHandler(
            UnauthorizedException.class
    )

    public ResponseEntity<ErrorResponse>
    handleUnauthorized(

            UnauthorizedException ex
    ) {

        ErrorResponse error =
                new ErrorResponse(

                        LocalDateTime.now(),

                        HttpStatus.UNAUTHORIZED.value(),

                        "Unauthorized",

                        ex.getMessage()
                );

        return new ResponseEntity<>(
                error,
                HttpStatus.UNAUTHORIZED
        );
    }

    // ACCESS DENIED
    @ExceptionHandler(
            AccessDeniedException.class
    )

    public ResponseEntity<ErrorResponse>
    handleAccessDenied(

            AccessDeniedException ex
    ) {

        ErrorResponse error =
                new ErrorResponse(

                        LocalDateTime.now(),

                        HttpStatus.FORBIDDEN.value(),

                        "Forbidden",

                        "You are not authorized to access this resource"
                );

        return new ResponseEntity<>(
                error,
                HttpStatus.FORBIDDEN
        );
    }

    // VALIDATION ERRORS
    @ExceptionHandler(
            MethodArgumentNotValidException.class
    )

    public ResponseEntity<Map<String, String>>
    handleValidationErrors(

            MethodArgumentNotValidException ex
    ) {

        Map<String, String> errors =
                new HashMap<>();

        ex.getBindingResult()
                .getFieldErrors()
                .forEach(error ->

                        errors.put(

                                error.getField(),

                                error.getDefaultMessage()
                        )
                );

        return new ResponseEntity<>(
                errors,
                HttpStatus.BAD_REQUEST
        );
    }

    // GENERIC EXCEPTION
    @ExceptionHandler(Exception.class)

    public ResponseEntity<ErrorResponse>
    handleGenericException(

            Exception ex
    ) {

        ErrorResponse error =
                new ErrorResponse(

                        LocalDateTime.now(),

                        HttpStatus.INTERNAL_SERVER_ERROR.value(),

                        "Internal Server Error",

                        ex.getMessage()
                );

        return new ResponseEntity<>(
                error,
                HttpStatus.INTERNAL_SERVER_ERROR
        );
    }
}