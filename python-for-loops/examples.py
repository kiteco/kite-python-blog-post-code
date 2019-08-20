"""
Example code from Python For Loops: Quick Answers and Examples

"""

# Basic Usage
word = 'Mississippi'
count = 0
for letter in word:
    if letter == 'i':
        count = count + 1
print(count)

# Lists
student_list = ("jake", "john", "jim")
for student in student_list:
    print(student)

# How do loops work?
for character in "Kite":
    print(character)

# iterating with next()
example_tuple = ("smartwater", "fiji", "aquafina")
my_tuple = iter(example_tuple)

print(next(my_tuple))
print(next(my_tuple))
print(next(my_tuple))

# with a loop
example_tuple = ("smartwater", "fiji", "aquafina")
for x in example_tuple:
    print(x)

# break statement
students = ["John", "Jerry", "Sarah"]
for x in students:
    print(x)
    if x == "Jerry":
        break

students = ["John", "Jerry", "Sarah"]
for x in students:
    if x == "Jerry":
        break
    print(x)

# continue statement
students = ["John", "Jerry", "Sarah"]
for x in students:
    if x == "Jerry":
        continue
    print(x)

# range()
for x in range(5):
    print(x)

for x in range(0, 10, 2):
    print(x)

# else
for x in range(5):
    print(x)
else:
    print("Finally finished!")

# non-nested loop
list_of_lists = [['yorkshire', 'jack russell', 'golden retriever'], [0, 1, 2], [11, 22, 33]]

for list_item in list_of_lists:
    print(list_item)

# nested loop
list_of_lists = [['yorkshire', 'jack russell', 'golden retriever'], [0, 1, 2], [11, 22, 33]]

for list_item in list_of_lists:
    for item in list_item:
        print(item)

# nesting for combination
adj = ["red", "sporty", "electric"]
cars = ["BMW", "Lexus", "Tesla"]

for x in adj:
    for y in cars:
        print(x, y)

# infinite loop
count = 0
i = 1
while i == 1:
    count += 1

# Calling range()
for i in range(6):
    print(i)

for i in range(1, 6):
    print(i)

for i in range(5):
    print(i + 1)
