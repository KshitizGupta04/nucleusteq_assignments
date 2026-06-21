# This file contains Q.35 to Q.39


# Question 35
# Create a file and write my name into it

def write_name():
    with open("student.txt", "w") as file:
        file.write("Kshitiz Gupta")

# Question 36
# Read a file and count words, lines, and characters
def file_statistics(file_name):
    with open(file_name, "r") as file:
        content = file.read()

    word_count = len(content.split())
    line_count = len(content.splitlines())
    character_count = len(content)

    print("Words:", word_count)
    print("Lines:", line_count)
    print("Characters:", character_count)



# Question 37
# Append data to existing file
def append_data(file_name, data):
    with open(file_name, "a") as file:
        file.write("\n" + data)



# Question 38
# Copy content from one file to another
def copy_file(source_file, destination_file):
    with open(source_file, "r") as source:
        content = source.read()

    with open(destination_file, "w") as destination:
        destination.write(content)


# Question 39
# Search a word in a file
def search_word(file_name, word):
    with open(file_name, "r") as file:
        content = file.read()

    if word in content:
        print("Word Found")
    else:
        print("Word Not Found")


# Driver Code
# Question 35
write_name()
print("student.txt created successfully")

# Question 36
print("\nFile Statistics:")
file_statistics("student.txt")

# Question 37
append_data("student.txt", "Python Training")
print("\nData appended successfully")

# Question 38
copy_file("student.txt", "backup.txt")
print("Content copied to backup.txt")

# Question 39
print("\nSearching Word:")
search_word("student.txt", "Kshitiz")