"""
Example Code for
"Python String Formatting"
"""

"""
The old way: printf style formatting
"""

# Insert values by indicating their type
this = "this"
five = 5
"%s is a %d" % (this, five)

# %s can be used with any object
"%s is a list" % [1, 2, 3]

# %r is the same as calling repr()
"%s sounds like %r" % ("Seaweed", "Seaweed")

# Pass in the number of desired digits
"%.3f" % 6.1234567

# Add padding by specifying number of characters
for w in ['some', 'words', 'are', 'longer']:
    print("|%15s" % w)

# Use a dictionary to insert values into the string
ship_info = {'ship': 'personiples', 'captain': 'Archaeus'}

"%(ship)s was run hard by %(captain)s" % ship_info

"""
Python 3: str.format() - (Curly Braces)
"""
"{} comes before {}".format('a', 'b')

# Specify the index for repeated arguments
"{1} is after {0} which is before {1}".format('a', 'b')

# Specify the argument by name
"{cat} loves {dog}, {dog} loves {cat}".format(cat='Whiskers', dog='Rover')

# Use dictionaries as named arguments
ship_captains = {'The Irish Rover': 'Mick McCann', 'Davey Crockett': 'Burgess'}
"{Davey Crockett} and {The Irish Rover} are both ship captains".format(**ship_captains)


# Access object attributes in replacement field
class Ship:
    def __init__(self, name, masts, captain):
        self.name = name
        self.masts = masts
        self.captain = captain

    def __str__(self):
        msg = "{self.name} had {self.masts} masts and was captained by {self.captain}"
        return msg.format(self=self)


# Create the ship objects
ships = [Ship("The Irish Rover", 27, 'Mick McCann'),
         Ship("Davey Crockett", 3, 'Burgess'),
         Ship("The John B", 2, 'Richard Le Gallienne')]

# Print() uses __str__ method
for ship in ships:
    print(ship)

# Add format specification
for ship in ships:
    print("|{ship.name:>22}|{ship.captain:>22}|{ship.masts:>22}|".format(ship=ship))

"""
F-Strings
"""
strings_count = 5
frets_count = 21
f"My banjo has {strings_count} strings and {frets_count} frets"

# Access contents of a list
arrivals = ['The Irish Rover', 'The Titanic', 'The Rueben']
f'The first to arrive was {arrivals[0]} and the last was {arrivals[-1]}'

# Specify a conversion type
ship_name = "Davey Crockett"
f'The ships name was spelled {ship_name!r}'

f'The ships name was spelled {repr(ship_name)}'

# ascii() function
check = "√"
f"The ascii version of {check} is {check!a}"

# nesting fields
rag_count = 1000000
padding = 10
f'Sligo rags: {rag_count:{padding}d}'
