# imports sqlite
import sqlite3

# connects it to the books-collection database
conn = sqlite3.connect('books-collection.db')

# creates the cursor
c = conn.cursor()

# execute the query which creates the table called books with id and name  #as the columns
c.execute('''
          CREATE TABLE books
          (id INTEGER PRIMARY KEY ASC, 
	     name varchar(250) NOT NULL)
          ''')

# executes the query which inserts values in the table
c.execute("INSERT INTO books VALUES(1, 'The Bell Jar')")

# commits the executions
conn.commit()

# closes the connection
conn.close()
