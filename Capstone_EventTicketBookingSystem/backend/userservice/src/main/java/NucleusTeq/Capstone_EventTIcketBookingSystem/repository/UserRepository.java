package NucleusTeq.Capstone_EventTIcketBookingSystem.repository;
import NucleusTeq.Capstone_EventTIcketBookingSystem.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
}
