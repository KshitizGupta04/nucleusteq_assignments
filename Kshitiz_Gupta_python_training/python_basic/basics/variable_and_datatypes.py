# this is file for Q.4 to Q.6

# Question 4
def show_datatypes() :
    integer_type=5
    float_type=10.00
    String_type="Kshitiz"
    boolean_type=False

    print(type(integer_type))
    print(type(float_type))
    print(type(String_type))
    print(type(boolean_type))

print(show_datatypes())

# Question 5
def swap_two_numbers() :
    number1=input("enter the first number : ")
    number2=input("enter the second number : ")
    
    print("the numbers before swapping is " +number1,number2)
    number1,number2=number2,number1
    print("the numbers after swappins is " +number1,number2)

print(swap_two_numbers())
