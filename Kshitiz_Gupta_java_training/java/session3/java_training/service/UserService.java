package nucleusteq.session3.java_training.service;

import lombok.AllArgsConstructor;
import nucleusteq.session3.java_training.model.User;
import nucleusteq.session3.java_training.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Objects;
import java.util.Optional;

@Service
@AllArgsConstructor
public class UserService {

    private final UserRepository repo;

//    public UserService(UserRepository repo) {
//        this.repo=repo;
//    }
public User submit(User user) {

    if (user.getName() == null || user.getName().isEmpty()) {
        throw new RuntimeException("Invalid name");
    }

    Integer age = user.getAge();

    if (user.getAge() == null || user.getAge() <= 0) {
        throw new RuntimeException("Invalid age");
    }

    if (user.getRole() == null || user.getRole().isEmpty()) {
        throw new RuntimeException("Invalid role");
    }

    return user;
}

    public List<User> search(String name, Integer age, String role) {
        List<User> list = repo.findAll();
        if(name!=null) {
            list=list.stream().filter(u->u.getName().equalsIgnoreCase(name)).toList();
        }

        if (age != null) {
            list = list.stream()
                    .filter(u -> Objects.equals(u.getAge(), age))
                    .toList();
        }

        if (role != null) {
            list = list.stream()
                    .filter(u -> u.getRole().equalsIgnoreCase(role))
                    .toList();
        }
        return list;
    }

    public String delete(Long id, Boolean confirm) {
        if (confirm == null || !confirm) {
            return "Confirmation required";
        }

        Optional<User> list = repo.findById(id);

        if (list.isEmpty()) {
            throw new RuntimeException("User not found");
        }

        repo.delete(list.get());

        return "User deleted successfully";
    }
}
