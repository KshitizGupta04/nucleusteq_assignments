# This file contains Q.40 to Q.44

# Question 40
# Create a Student class with attributes and display details
class Student:
    def __init__(self, name, age, course):
        self.name = name
        self.age = age
        self.course = course

    def display_details(self):
        print("Name:", self.name)
        print("Age:", self.age)
        print("Course:", self.course)



# Question 41
# Create a Car class with a constructor
class Car:
    def __init__(self, company, model):
        self.company = company
        self.model = model

    def display_car(self):
        print("Company:", self.company)
        print("Model:", self.model)


# Question 42
# Implement inheritance using Person and Employee class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Employee(Person):
    def __init__(self, name, age, salary):
        super().__init__(name, age)
        self.salary = salary

    def display_employee(self):
        print("Name:", self.name)
        print("Age:", self.age)
        print("Salary:", self.salary)



# Question 43
# Implement encapsulation using private variables in Bank class
class Bank:
    def __init__(self, balance):
        self.__balance = balance

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance



# Question 44
# Demonstrate polymorphism using same method name
class Dog:
    def sound(self):
        print("Dog barks")


class Cat:
    def sound(self):
        print("Cat meows")


# Driver Code
# Question 40
student = Student("Kshitiz", 21, "B.Tech")
student.display_details()

# Question 41
car = Car("Toyota", "Fortuner")
car.display_car()

# Question 42
employee = Employee("Kshitiz", 25, 50000)
employee.display_employee()

# Question 43
account = Bank(10000)
account.deposit(5000)
print("Balance:", account.get_balance())

# Question 44
dog = Dog()
cat = Cat()

dog.sound()
cat.sound()