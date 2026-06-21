#this file contains Q.22 to Q.24

# Question 22
'''basic arithmetic operations using math module'''
import math
def arithmetic_math_module() :
    num=int(input("enter the number : "))
    power_number=math.pow(num,3)
    squareroot_number=math.sqrt(num)
    factorial_num=math.factorial(num)

    print(power_number)
    print(squareroot_number)
    print(factorial_num)

arithmetic_math_module()

# Question 23
'''generating a random value from a given range'''
import random
def generate_random(value) :
    random_value=random.randint(1,value)
    print(random_value)

generate_random(1200)

# Question 24
'''created custom module and imported here to use'''
import custom_module
print(custom_module.find_square(7))
print(custom_module.is_Palindrome("indore"))


