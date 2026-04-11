package com.Kshitiz.java_training.controller;

import com.Kshitiz.java_training.model.User;
import com.Kshitiz.java_training.service.UserService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }


    @GetMapping
    public List<User> getUsers() {
        return userService.getAllUsers();
    }


    @PostMapping
    public User createUser(@RequestBody User user) {
        return userService.createUser(user);
    }


    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.getUserById(id);
    }
}