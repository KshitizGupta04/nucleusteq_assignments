package com.nucleusteq.todoapp.service;

import com.nucleusteq.todoapp.dto.TodoDTO;
import com.nucleusteq.todoapp.entity.Todo;
import com.nucleusteq.todoapp.entity.TodoStatus;
import com.nucleusteq.todoapp.exception.ResourceNotFoundException;
import com.nucleusteq.todoapp.repository.TodoRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class TodoServiceImplTest {

    @Mock
    private TodoRepository todoRepository;

    @Mock
    private NotificationServiceClient notificationServiceClient;

    @InjectMocks
    private TodoServiceImpl todoService;

    @Test
    void shouldCreateTodo() {

        TodoDTO dto = new TodoDTO();
        dto.setTitle("Learn Spring");
        dto.setDescription("Practice Spring Boot");

        Todo savedTodo = new Todo();
        savedTodo.setId(1L);
        savedTodo.setTitle("Learn Spring");
        savedTodo.setDescription("Practice Spring Boot");
        savedTodo.setStatus(TodoStatus.PENDING);
        savedTodo.setCreatedAt(LocalDateTime.now());

        when(todoRepository.save(any(Todo.class)))
                .thenReturn(savedTodo);

        TodoDTO result = todoService.createTodo(dto);

        assertNotNull(result);
        assertEquals("Learn Spring", result.getTitle());

        verify(todoRepository, times(1))
                .save(any(Todo.class));

        verify(notificationServiceClient, times(1))
                .sendNotification(anyString());
    }

    @Test
    void shouldReturnAllTodos() {

        Todo todo1 = new Todo();
        todo1.setId(1L);
        todo1.setTitle("Todo 1");

        Todo todo2 = new Todo();
        todo2.setId(2L);
        todo2.setTitle("Todo 2");

        when(todoRepository.findAll())
                .thenReturn(Arrays.asList(todo1, todo2));

        assertEquals(
                2,
                todoService.getAllTodos().size()
        );
    }

    @Test
    void shouldReturnTodoById() {

        Todo todo = new Todo();
        todo.setId(1L);
        todo.setTitle("Learn Testing");

        when(todoRepository.findById(1L))
                .thenReturn(Optional.of(todo));

        TodoDTO result =
                todoService.getTodoById(1L);

        assertEquals(
                "Learn Testing",
                result.getTitle()
        );
    }

    @Test
    void shouldThrowExceptionWhenTodoNotFound() {

        when(todoRepository.findById(100L))
                .thenReturn(Optional.empty());

        assertThrows(
                ResourceNotFoundException.class,
                () -> todoService.getTodoById(100L)
        );
    }

    @Test
    void shouldUpdateTodo() {

        Todo existingTodo = new Todo();
        existingTodo.setId(1L);
        existingTodo.setTitle("Old");
        existingTodo.setStatus(TodoStatus.PENDING);

        TodoDTO dto = new TodoDTO();
        dto.setTitle("New");
        dto.setDescription("Updated");
        dto.setStatus(TodoStatus.COMPLETED);

        when(todoRepository.findById(1L))
                .thenReturn(Optional.of(existingTodo));

        when(todoRepository.save(any(Todo.class)))
                .thenReturn(existingTodo);

        TodoDTO result =
                todoService.updateTodo(1L, dto);

        assertEquals("New", result.getTitle());
    }

    @Test
    void shouldDeleteTodo() {

        Todo todo = new Todo();
        todo.setId(1L);

        when(todoRepository.findById(1L))
                .thenReturn(Optional.of(todo));

        todoService.deleteTodo(1L);

        verify(todoRepository, times(1))
                .delete(todo);
    }

    @Test
    void shouldThrowExceptionWhenStatusIsSame() {

        Todo todo = new Todo();
        todo.setId(1L);
        todo.setTitle("Test");
        todo.setStatus(TodoStatus.PENDING);

        TodoDTO dto = new TodoDTO();
        dto.setTitle("Test");
        dto.setStatus(TodoStatus.PENDING);

        when(todoRepository.findById(1L))
                .thenReturn(Optional.of(todo));

        assertThrows(
                IllegalArgumentException.class,
                () -> todoService.updateTodo(1L, dto)
        );
    }
}