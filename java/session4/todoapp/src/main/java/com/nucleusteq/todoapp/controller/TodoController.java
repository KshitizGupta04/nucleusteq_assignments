package com.nucleusteq.todoapp.controller;

import com.nucleusteq.todoapp.dto.TodoDTO;
import com.nucleusteq.todoapp.service.TodoService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@RestController
@RequestMapping("/todos")
public class TodoController {

    private final TodoService todoService;

    public TodoController(TodoService todoService) {
        this.todoService=todoService;
    }

    @PostMapping
    public ResponseEntity<TodoDTO> createDTO(@Valid @RequestBody TodoDTO todoDTO) {
        return new ResponseEntity<>(todoService.createTodo(todoDTO), HttpStatus.CREATED);
    }

    @GetMapping
    public ResponseEntity<List<TodoDTO>> getALlTodos() {
        return ResponseEntity.ok(todoService.getAllTodos());
    }

    @GetMapping("/{id}")
    public ResponseEntity<TodoDTO> getTodoById(@PathVariable Long id) {
        return ResponseEntity.ok(todoService.getTodoById(id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<TodoDTO> updateTodo(@PathVariable Long id,@Valid @RequestBody TodoDTO todoDTO) {
        return ResponseEntity.ok(todoService.updateTodo(id,todoDTO));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteTodo(
            @PathVariable Long id) {

        todoService.deleteTodo(id);

        return ResponseEntity.ok(
                "Todo Deleted Successfully"
        );
    }


}
