package com.nucleusteq.todoapp.service;

import com.nucleusteq.todoapp.dto.TodoDTO;

import java.util.List;

public interface TodoService {
    TodoDTO createTodo(TodoDTO todoDTO );
    List<TodoDTO> getAllTodos();
    TodoDTO getTodoById(Long id);
    TodoDTO updateTodo(Long id,TodoDTO todoDTO);
    void deleteTodo(Long id);
}
