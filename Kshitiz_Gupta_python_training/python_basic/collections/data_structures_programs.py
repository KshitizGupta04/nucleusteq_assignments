# Question 25
def list_operations(list_number) :
    sum=0
    largest=float('-inf')

    # (a) find sum
    for i in range(0,len(list_number)) :
        sum=sum+list_number[i]
    print(sum)
    
    # (b) find largest
    for i in range(0,len(list_number)) :
        largest=max(largest,list_number[i])
    print(largest)

    # (c) sort the list
    sort=sorted(list_number)
    print(sort)

    # (d) remove duplicate
    unique_number=list(set(list_number))
    print(unique_number)

# Question 26
'''for counting off and even values in list'''
def count_even_and_odd(list_values) :
    counteven=0
    countodd=0
    for i in range(0,len(list_values)) :
        if list_values[i]%2==0 :
            counteven = counteven+1
        else :
            countodd=countodd+1
    
    print(counteven)
    print(countodd)

# Question 27
'''reverse the list without using inbuilt reverse function'''
def rev_list(list_value) :
    start=0
    end=len(list_value)-1
    while start < end :
        list_value[start],list_value[end]=list_value[end],list_value[start]
        start=start+1
        end=end-1
    print(list_value)

# Question 28
'''create and accessing the values of tuple'''
def access_tuple() :
    tuple_number=(1,7,4,8)
    for i in tuple_number :
        print(i)

# Question 29
'''converting the tuple into list for modification as tuples are immutable'''
def tuple_into_list(tuple_value) :
    list_value=list(tuple_value)
    list_value[0]=7
    print(list_value)

# Question 30
'''performing different set operations'''
def set_operations(set1,set2) :
    union_set=set1 | set2
    intersection_set=set1 & set2
    difference_set=set1 - set2

    print(union_set)
    print(intersection_set)
    print(difference_set)

# Question 31
'''removing duplicates from list using set'''
def remove_duplicate(list_value) :
    set1=set(list_value)
    final_list=list(set1)
    print(final_list)

# Question 32
'''creating and accesing the dictionary datatype'''
def display_student(student):
    print("Name:", student["name"])
    print("Roll No:", student["roll_no"])
    print("Course:", student["course"])
    print("Marks:", student["marks"])

# Question 33
# counting frequency using dictionary
def count_frequency(s):
    freq = {}

    for ch in s:
        if ch in freq:
            freq[ch] += 1
        else:
            freq[ch] = 1

    print(freq)

# Question 34
# merging two dictionaries to form a single resultant dictionary
def merge_dict(d1, d2):
    d3 = d1.copy()
    
    for key, value in d2.items():
        d3[key] = value
    
    print("Merged Dictionary:", d3)



#driver code
list_operations([1,2,6,4,3,2,4,3,7,9])
count_even_and_odd([1,2,6,4,3,2,4,3,7,9])
rev_list([1,2,6,4,3,2,4,3,7,9])
access_tuple()
tuple_into_list((1,7,4,8))

set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
set_operations(set1,set2)

remove_duplicate([1,2,6,4,3,2,4,3,7,9])

student = {
    "name": "Kshitiz",
    "roll_no": 101,
    "course": "B.Tech",
    "marks": 85
}
display_student(student)
count_frequency("Kshitiz")

d1 = {"a": 1, "b": 2}
d2 = {"c": 3, "d": 4}
merge_dict(d1, d2)
