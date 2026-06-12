package com.nucleusteq.todoapp.controller;

import com.nucleusteq.todoapp.dto.TodoDTO;
import com.nucleusteq.todoapp.service.TodoService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

@RestController
@RequestMapping("/todos")
public class TodoController {

    private static final Logger logger =
            LoggerFactory.getLogger(TodoController.class);

    private final TodoService todoService;

    public TodoController(TodoService todoService) {
        this.todoService = todoService;
    }

    @PostMapping
    public ResponseEntity<TodoDTO> createTodo(
            @Valid @RequestBody TodoDTO todoDTO) {

        logger.info("Creating new todo");

        return new ResponseEntity<>(
                todoService.createTodo(todoDTO),
                HttpStatus.CREATED
        );
    }

    @GetMapping
    public ResponseEntity<List<TodoDTO>> getALlTodos() {

        logger.info("Fetching all todos");

        return ResponseEntity.ok(
                todoService.getAllTodos()
        );
    }

    @GetMapping("/{id}")
    public ResponseEntity<TodoDTO> getTodoById(
            @PathVariable Long id) {

        logger.info("Fetching todo with id: {}", id);

        return ResponseEntity.ok(
                todoService.getTodoById(id)
        );
    }

    @PutMapping("/{id}")
    public ResponseEntity<TodoDTO> updateTodo(
            @PathVariable Long id,
            @Valid @RequestBody TodoDTO todoDTO) {

        logger.info("Updating todo with id: {}", id);

        return ResponseEntity.ok(
                todoService.updateTodo(id, todoDTO)
        );
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteTodo(
            @PathVariable Long id) {

        logger.info("Deleting todo with id: {}", id);

        todoService.deleteTodo(id);

        return ResponseEntity.ok(
                "Todo Deleted Successfully"
        );
    }
}