# this file contain Q.17 to Q.20

# Question 17
'''calculating the square of the number'''
def find_square(number):
    return number * number


# Question 18
'''checking if the palindrome exist or not for a string'''
def isPalindrome(s):
    start = 0
    end = len(s) - 1

    while start < end:
        if s[start] != s[end]:
            return False

        start += 1
        end -= 1

    return True


# Question 19
'''finding the maximum number in a list'''
def max_list(numbers):
    largest = float('-inf')

    for i in range(len(numbers)):
        largest = max(largest, numbers[i])

    return largest


# Question 20
'''demostrate the basic use of the default parameters'''
def default_param(name, city="Khargone"):
    return f"{name} lives in {city}"


# Driver Code
print("Square:", find_square(8))

if isPalindrome("KshsK"):
    print("Palindrome")
else:
    print("Not Palindrome")

values = [15,84,23,272,111]
print("Maximum Number:", max_list(values))

print(default_param("Kshitiz"))
print(default_param("Kunjesh", "Indore"))