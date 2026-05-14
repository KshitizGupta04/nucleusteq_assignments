package NucleusTeq.Capstone_EventTIcketBookingSystem.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;

import org.springframework.stereotype.Component;

import java.util.Date;

@Component
public class JwtUtil {

    private static final String SECRET_KEY =
            "myverystrongsecretkeymyverystrongsecretkey12345";

    // Generate JWT Token
    public String generateToken(String email) {

        return Jwts.builder()

                .setSubject(email)

                .setIssuedAt(new Date())

                .setExpiration(
                        new Date(System.currentTimeMillis()
                                + 1000 * 60 * 60)
                )

                .signWith(
                        SignatureAlgorithm.HS256,
                        SECRET_KEY.getBytes()
                )

                .compact();
    }

    // Extract Email
    public String extractEmail(String token) {

        return extractClaims(token).getSubject();
    }

    // Validate Token
    public boolean validateToken(String token) {

        try {

            return !extractClaims(token)
                    .getExpiration()
                    .before(new Date());

        } catch (Exception e) {

            return false;
        }
    }

    // Extract Claims
    private Claims extractClaims(String token) {

        return Jwts.parser()

                .setSigningKey(SECRET_KEY.getBytes())

                .parseClaimsJws(token)

                .getBody();
    }
}