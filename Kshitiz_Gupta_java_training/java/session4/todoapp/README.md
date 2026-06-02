# TODO Application

## Overview

This project is a TODO Management Application developed using Spring Boot. It demonstrates the implementation of RESTful APIs, layered architecture, JPA, DTO mapping, validation, logging, exception handling, and unit testing using JUnit and Mockito.

The application allows users to create, retrieve, update, and delete TODO items while following enterprise-level development practices.

---

## Technologies Used

* Java 17
* Spring Boot
* Spring Data JPA (Hibernate)
* Maven
* H2 Database
* JUnit 5
* Mockito
* SLF4J Logging

---

## Project Architecture

The application follows a layered architecture:

Controller → Service → Repository → Database

### Layers

#### Controller Layer

Handles incoming HTTP requests and returns responses.

#### Service Layer

Contains business logic and application rules.

#### Repository Layer

Performs database operations using JPA Repository.

#### DTO Layer

Transfers data between client and server without exposing entities directly.

#### Entity Layer

Represents database tables and persistent data.

---

## Features

### Create TODO

Create a new TODO item.

### Get All TODOs

Retrieve all available TODO items.

### Get TODO By ID

Retrieve a specific TODO item using its ID.

### Update TODO

Update title, description, or status of a TODO item.

### Delete TODO

Delete an existing TODO item.

---

## Spring Concepts Demonstrated

### Inversion of Control (IoC)

Spring manages application components and object lifecycle.

### Dependency Injection

Constructor-based dependency injection is used throughout the project.

### Component Scanning

Spring automatically detects and registers components using annotations.

### Annotation Usage

The project demonstrates the use of:

* @RestController
* @Service
* @Repository
* @Entity
* @Table
* @Id
* @GeneratedValue
* @Valid
* @RequestMapping
* @GetMapping
* @PostMapping
* @PutMapping
* @DeleteMapping

---

## Validation

Input validation is implemented using Jakarta Validation.

Example:

* Title cannot be null
* Title must contain at least 3 characters

---

## Logging

SLF4J Logger is implemented in:

### Controller Layer

Logs API requests such as:

* Creating TODO
* Fetching TODOs
* Updating TODOs
* Deleting TODOs

### Service Layer

Logs business operations such as:

* TODO creation
* TODO update
* TODO deletion
* TODO retrieval

---

## Exception Handling

Global exception handling is implemented using:

* ResourceNotFoundException
* GlobalExceptionHandler

Handled scenarios:

* Invalid TODO ID
* Validation failures
* Illegal status transitions

---

## Notification Service

A dummy NotificationServiceClient has been implemented to simulate communication with an external service.

Whenever a new TODO is created:

Notification sent for new TODO

is triggered from the Service Layer.

---

## Testing

Unit testing is implemented using:

* JUnit 5
* Mockito

### Tested Components

* TodoServiceImpl

### Test Coverage

The Service Layer achieves more than 85% code coverage.

Test cases cover:

* Create TODO
* Get TODO By ID
* Get All TODOs
* Update TODO
* Delete TODO
* Exception Scenarios

---

## API Endpoints

### Create TODO

POST /todos

### Get All TODOs

GET /todos

### Get TODO By ID

GET /todos/{id}

### Update TODO

PUT /todos/{id}

### Delete TODO

DELETE /todos/{id}

---

## Build and Run

### Run Tests

mvn test

### Build Project

mvn clean install

### Run Application

mvn spring-boot:run

---

## Author

Kshitiz Gupta

Session 4 Assignment - Enterprise Flow and Testing
