package com.nucleusteq.todoapp.dto;

import com.nucleusteq.todoapp.entity.TodoStatus;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.time.LocalDateTime;

public class TodoDTO {
    @NotNull(message = "title cannot be null")
    @Size(min=3,message = "title must contain at least 3 character")

    private String title;
    private String description;
    private TodoStatus status;
    private Long id;
    private LocalDateTime createdAt;

    public TodoDTO() {

    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String tittle) {
        this.title=tittle;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description=description;
    }

    public TodoStatus getStatus() {
        return status;
    }

    public void setStatus(TodoStatus status) {
        this.status=status;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id=id;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt=createdAt;
    }
}
