"""
Dictionary Creation
"""
my_dict = {'key1': 1, 'key2': 2}

my_dict = dict(key1=1, key2=2)

my_dict = {}

my_dict = dict()

my_dict['key'] = 123

# Define a dict with some string values and keys
my_dict = {
    'my_nested_dict':
        {
            'a_key': 'a_value',
            'another_key': 'another_value',
        }
}

my_variable = my_dict['my_nested_dict']

"""
Practical Use Cases
"""


class User(object):
    """  Stores info about Users """

    def __init__(self, name, email, address, password, url):
        self.name = name
        self.email = email
        ...

    def send_email(self):
        """ Send an email to our user"""
        pass

    def __repr__():
        """Logic to properly format data"""


bill = User('bill @ gmail.com', '123 Acme Dr.', 'secret-password',
            'http: // www.bill.com')
bill.send_email()

bill = {'email': 'bill@gmail.com',
        'address': '123 Acme Dr.',
        'password': 'secret-password',
        'url': 'http://www.bill.com'}


def send_email(user_dict):
    pass


# smtp email logic …

send_email(bill['email'])  # bracket notation or …
send_email(bill.get('email'))  # .get() method is handy, too

# Sample user data

json_response = [{
    "id": 1,
    "first_name": "Florentia",
    "last_name": "Schelle",
    "email": "fschelle0@nyu.edu",
    "url": "https://wired.com"
}, {
    "id": 2,
    "first_name": "Montague",
    "last_name": "McAteer",
    "email": "mmcateer1@zdnet.com",
    "url": "https://domainmarket.com"
}, {
    "id": 3,
    "first_name": "Dav",
    "last_name": "Yurin",
    "email": "dyurin2@e-recht24.de",
    "url": "http://wufoo.com"
}]

users = []
for i in json_response:
    users.append(User(
        name=i['first_name'] + i['last_name'],
        email = i['email'],
        url=i['url'],
        # ...
    ))
