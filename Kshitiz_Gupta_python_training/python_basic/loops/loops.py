# this file from Q.12 to Q.16

# Question 12
def one_to_hundred() :
        for i in range(1,101) : 
                print(i)

one_to_hundred()

# Question 13
def multiplication_table() :
        num=int(input("enter the number : "))
        for i in range(1,11) :
                print(f"the {num}*{i} is {num*i}")

multiplication_table()

# Question 14
def factorial() :
        fact=int(input("enter the number : "))
        prod=1
        for i in range(1,fact+1) :
                prod=prod*i
        print(prod)

factorial()
        