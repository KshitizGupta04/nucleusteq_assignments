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

        
# Question 15
def reverse() :
        num=int(input("enter the number :"))
        rev=0
        while num > 0 :
                rem=num%10
                rev=rev*10+rem
                num=num//10
        print(rev)

reverse()

# Question 16
def is_prime() :
        num=int(input("enter the number"))
        if(num==0 or num==1) :
                print("Not a prime no")
                return

        flag=False
        for i in range(2,num) :
                if(num%i==0) :
                        flag=True
                        print("Number is not prime")
                        break
                
        
        if(flag==False) :
                print("Number is prime number")

is_prime()

                
