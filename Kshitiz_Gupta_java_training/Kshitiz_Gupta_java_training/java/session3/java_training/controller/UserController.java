package nucleusteq.session3.java_training.controller;

import nucleusteq.session3.java_training.model.User;
import nucleusteq.session3.java_training.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/users")


public class UserController {
    private final UserService service;

    public UserController(UserService service) {
        this.service = service;
    }

    @GetMapping("/test")
    public String test() {
        return "Working";
    }

    @GetMapping("/search")
    public List<User> search(
        @RequestParam(required = false) String name,
        @RequestParam(required = false) Integer age,
        @RequestParam(required = false) String role
    ) {
        return service.search(name, age, role);
    }

    @DeleteMapping("/{id}")
    public String delete(@PathVariable Long id,
                         @RequestParam(required=false) Boolean confirm
    ) {
        return service.delete(id,confirm);
    }

    @PostMapping("/submit")
    public ResponseEntity<String> submit(@RequestBody User user) {
        try {
            service.submit(user);
            return ResponseEntity.status(201).body("User submitted successfully");
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

}
