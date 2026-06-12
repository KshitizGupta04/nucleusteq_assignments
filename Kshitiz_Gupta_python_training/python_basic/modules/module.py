


# Question 22
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
import random
def generate_random(value) :
    random_value=random.randint(1,value)
    print(random_value)

generate_random(1200)

# Question 24
import custom_module
print(custom_module.find_square(7))
print(custom_module.is_Palindrome("indore"))

