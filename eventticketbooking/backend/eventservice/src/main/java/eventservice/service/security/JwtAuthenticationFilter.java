package eventservice.service.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.security.Key;
import java.util.Collections;

@Component
public class JwtAuthenticationFilter
        extends OncePerRequestFilter {

    @Value("${jwt.secret}")
    private String secretKey;

    private Key getSigningKey() {

        return Keys.hmacShaKeyFor(
                secretKey.getBytes()
        );
    }

    @Override
    protected void doFilterInternal(

            HttpServletRequest request,

            HttpServletResponse response,

            FilterChain filterChain

    ) throws ServletException, IOException {

        String authHeader =
                request.getHeader("Authorization");

        String email = null;

        String token = null;

        try {

            if (
                    authHeader != null
                            &&
                            authHeader.startsWith("Bearer ")
            ) {

                token =
                        authHeader.substring(7);

                Claims claims =

                        Jwts.parserBuilder()

                                .setSigningKey(
                                        getSigningKey()
                                )

                                .build()

                                .parseClaimsJws(token)

                                .getBody();

                email =
                        claims.getSubject();

                String role =
                        claims.get(
                                "role",
                                String.class
                        );

                // FIX ROLE ISSUE
                if (
                        role != null
                                &&
                                !role.startsWith("ROLE_")
                ) {

                    role = "ROLE_" + role;
                }

                SimpleGrantedAuthority authority =

                        new SimpleGrantedAuthority(
                                role
                        );

                UsernamePasswordAuthenticationToken authToken =

                        new UsernamePasswordAuthenticationToken(

                                email,

                                null,

                                Collections.singletonList(
                                        authority
                                )
                        );

                authToken.setDetails(

                        new WebAuthenticationDetailsSource()

                                .buildDetails(request)
                );

                SecurityContextHolder
                        .getContext()
                        .setAuthentication(authToken);
            }

        } catch (Exception e) {

            SecurityContextHolder.clearContext();
        }

        filterChain.doFilter(
                request,
                response
        );
    }
}