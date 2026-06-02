package com.nucleusteq.todoapp.service;

import com.nucleusteq.todoapp.dto.TodoDTO;
import com.nucleusteq.todoapp.entity.Todo;
import com.nucleusteq.todoapp.entity.TodoStatus;
import com.nucleusteq.todoapp.exception.ResourceNotFoundException;
import com.nucleusteq.todoapp.repository.TodoRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class TodoServiceImpl implements TodoService {

    private static final Logger logger =
            LoggerFactory.getLogger(TodoServiceImpl.class);

    private final TodoRepository todoRepository;
    private final NotificationServiceClient notificationServiceClient;

    public TodoServiceImpl(
            TodoRepository todoRepository,
            NotificationServiceClient notificationServiceClient) {

        this.todoRepository = todoRepository;
        this.notificationServiceClient = notificationServiceClient;
    }

    @Override
    public TodoDTO createTodo(TodoDTO todoDTO) {

        logger.info("Creating new todo with title: {}", todoDTO.getTitle());

        Todo todo = convertToEntity(todoDTO);

        todo.setCreatedAt(LocalDateTime.now());

        if (todo.getStatus() == null) {
            todo.setStatus(TodoStatus.PENDING);
        }

        Todo savedTodo = todoRepository.save(todo);

        notificationServiceClient.sendNotification(
                "Notification sent for new TODO"
        );

        logger.info("Todo created successfully with id: {}", savedTodo.getId());

        return convertToDTO(savedTodo);
    }

    @Override
    public List<TodoDTO> getAllTodos() {

        logger.info("Fetching all todos");

        return todoRepository.findAll()
                .stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public TodoDTO getTodoById(Long id) {

        logger.info("Fetching todo with id: {}", id);

        Todo todo = todoRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Todo not found with id : " + id));

        return convertToDTO(todo);
    }

    @Override
    public TodoDTO updateTodo(Long id, TodoDTO todoDTO) {

        logger.info("Updating todo with id: {}", id);

        Todo todo = todoRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Todo not found with id : " + id));

        todo.setTitle(todoDTO.getTitle());
        todo.setDescription(todoDTO.getDescription());

        if (todoDTO.getStatus() != null) {

            validateStatusTransition(
                    todo.getStatus(),
                    todoDTO.getStatus()
            );

            todo.setStatus(todoDTO.getStatus());
        }

        Todo updatedTodo = todoRepository.save(todo);

        logger.info("Todo updated successfully with id: {}", id);

        return convertToDTO(updatedTodo);
    }

    @Override
    public void deleteTodo(Long id) {

        logger.info("Deleting todo with id: {}", id);

        Todo todo = todoRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Todo not found with id : " + id));

        todoRepository.delete(todo);

        logger.info("Todo deleted successfully with id: {}", id);
    }

    private TodoDTO convertToDTO(Todo todo) {

        TodoDTO dto = new TodoDTO();

        dto.setId(todo.getId());
        dto.setTitle(todo.getTitle());
        dto.setDescription(todo.getDescription());
        dto.setStatus(todo.getStatus());
        dto.setCreatedAt(todo.getCreatedAt());

        return dto;
    }

    private Todo convertToEntity(TodoDTO dto) {

        Todo todo = new Todo();

        todo.setTitle(dto.getTitle());
        todo.setDescription(dto.getDescription());
        todo.setStatus(dto.getStatus());

        return todo;
    }

    private void validateStatusTransition(
            TodoStatus oldStatus,
            TodoStatus newStatus) {

        if (oldStatus.equals(newStatus)) {
            throw new IllegalArgumentException(
                    "Status is already " + oldStatus
            );
        }
    }
}