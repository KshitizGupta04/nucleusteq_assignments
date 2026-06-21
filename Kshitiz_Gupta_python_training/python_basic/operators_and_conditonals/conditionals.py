#this if file for Q.7 to Q.11

# Question 7
'''checking if the number is even or odd'''
def even_and_odd() :
    num=int(input("Enter the number :"))

    if(num%2==0) :
        print("number is even")
    else :
        print("number is odd")

even_and_odd()   

# Question 8
'''finding if the number is positive,negative or zero'''
def number_sign() :
    num=int(input("Enter the number :"))
    if(num>0) :
        print("number is positive")
    elif(num<0) :
        print("number is negative")
    else :
        print("number is zero")
    
number_sign()

# Question 9
'''finding the largest no among three numbers'''
def largest_number() :
    num1=int(input("enter the first number : "))
    num2=int(input("enter the second number : "))
    num3=int(input("enter the third number : "))

    if(num1>=num3 and num1>=num2) :
        print(f"{num1} is highest")
    elif(num2>=num3) :
        print(f"{num2} is highest")
    else :
        print(f"{num3} is highest")

largest_number()

# Question 10
'''allocating grades as per marks'''
def marks_to_grade() :
    marks=int(input("enter the marks :"))
    if(marks>100 or marks<0) :
        print("Please enter the correct marks")
    elif(marks>80 and marks<=100) :
        print("your grade is A")
    elif(marks>60 and marks<=80) :
        print("your grade is B")
    elif(marks>40 and marks<=60) :
        print("your grade is C")
    else :
        print("You are fail")
    
marks_to_grade()

# Question 11
'''finding if the year is leap year or not'''
def leap_year() :
    year=int(input("enter the year"))
    if(year%400==0) or (year%4==0 and year%100!=0) :
        print(f"{year} is a leap year")
    else :
        print(f"{year} is not leap year")

leap_year()
