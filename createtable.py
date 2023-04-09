# creating a table and a databse to store the stock symbols and notification email or number
import psycopg2 as ps

# connect to postgres db
try:
    conn = ps.connect('host=127.0.0.1  \
                      dbname= postgres \
                      user = postgres  \
                      password = 1234'
                      )
    conn.set_session(autocommit=True)
except ps.Error as e:
    print (e)

# using connection to get cursor 
try:
    cur = conn.cursor()
except ps.Error as e:
    print (e)


# creating a new database 
try:
    cur.execute('drop database if exists stockalert ')
    cur.execute("create database stockalert")
except ps.Error as e:
    print (e)

# close connection to postgres db
conn.close()

# connect to stockalert db
try:
    conn = ps.connect('host=127.0.0.1  \
                      dbname= stockalert \
                      user = postgres  \
                      password = 1234'
                      )
    conn.set_session(autocommit=True)
    print('db created')
except ps.Error as e:
    print (e)

# using connection to get cursor 
try:
    cur = conn.cursor()
except ps.Error as e:
    print (e)

# creating table
try:
    cur.execute('CREATE TABLE IF NOT EXISTS stock_subscriber(id serial primary key,symbol varchar(10),\
                contact_type varchar(2),contact_info varchar(50),upper int, lower int, frequency int,\
                 current_hour int default 0);')
    print('table created')
except ps.Error as e:
    print (e)

# close connection
conn.close()