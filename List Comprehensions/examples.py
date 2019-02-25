"""
List Comprehensions Examples
"""

my_list = []
# my_list.append()
# my_list.extend()


"""
When to use ListComps
"""
phones = [
    {
        'number': '111-111-1111',
        'label': 'phone',
        'extension': '1234',
    },

    {
        'number': '222-222-2222',
        'label': 'mobile',
        'extension': None,
    }
]

my_phone_list = []
for phone in phones:
    my_phone_list.append(phone['number'])

# List Comprehension
[phone['number'] for phone in phones]

"""
Advanced Usage
"""

# Buld an explicit nested list
table = [
    [1, 2, 3],
    [1, 2, 3],
    [1, 2, 3],
]

fields = ['x', 'y', 'z']
rows = [1, 2, 3]

table = []
for r in rows:
    row = []
    for field in fields:
        row.append(field)
    table.append(row)

[field for field in fields]
[row for row in rows]


table = [[field for field in fields] for row in rows]

"""
Dictionary Comprehensions
"""


[{str(item): item} for item in [1, 2, 3, ]]

dict1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

double_dict1 = {k: v * 2 for (k, v) in dict1.items()}

dict_map = {
	'apple' : 1,
	'cherry': 2,
	'earwax': 3,
}


{v:k for (k, v) in dict_map.items()}

items = dict_map.items()


"""
Logical Comparisons
"""



values = [1,2,3]
[i for i in values if i < 3]

[k for k, v in dict_map.items() if v < 3]


"""
Performance, Spongecase Example
"""

original_string = 'hello world'
spongecase_letters = []
for index, letter in enumerate(original_string):
    if index % 2 == 1:
        spongecase_letters.append(letter.upper())
    else:
        spongecase_letters.append(letter)
spongecase_string = ''.join(spongecase_letters)


# hElLo wOrLd

def spongecase(index, letter):
    if index % 2 == 1:
        return letter.upper()
    else:
        return letter


original_string = 'hello world'
spongecase_letters = []
for index, letter in enumerate(original_string):
    transformed_letter = spongecase(index, letter)
    spongecase_letters.append(transformed_letter)
spongecase_string = ''.join(spongecase_letters)
# hElLo wOrLd
