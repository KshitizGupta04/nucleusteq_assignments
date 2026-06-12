package nucleusteq.session3.java_training.repository;

import java.util.*;
import nucleusteq.session3.java_training.model.User;
import org.springframework.stereotype.Repository;

@Repository
public class UserRepository {
    private List<User> dummyUser = new ArrayList<>();


    public UserRepository() {
        dummyUser.add(new User(101L,"raj",18,"USER"));
        dummyUser.add(new User(102L,"Kshitiz",21,"ADMIN"));
        dummyUser.add(new User(103L,"Vishal",22,"USER"));
        dummyUser.add(new User(104L,"Purnesh",22, "ADMIN"));
        dummyUser.add(new User(105L,"Yash",21,"USER"));
    }

    public List<User> findAll() {
        return dummyUser;
    }

    public Optional<User> findById(Long id) {
        return dummyUser.stream().filter(u->u.getId().equals(id)).findFirst();
    }

    public void delete(User user) {
        dummyUser.remove(user);
    }




}
