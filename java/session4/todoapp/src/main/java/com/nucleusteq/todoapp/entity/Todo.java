package com.nucleusteq.todoapp.entity;

import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
@Table(name="todos")
public class Todo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;

    private String description;

    @Enumerated(EnumType.STRING)
    private TodoStatus status;

    private LocalDateTime createdAt;

    public Todo() {

    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id=id;
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

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt=createdAt;
    }
}
