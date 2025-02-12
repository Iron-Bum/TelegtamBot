import sqlite3


conn = sqlite3.connect('database/users.db')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS clients(
id INT,
name TEXT,
phone INT
); 
''')
cur.execute('''
CREATE TABLE IF NOT EXISTS services(
id INT,
name TEXT,
price INT NOT NULL DEFAULT '0.00'
); 
''')
cur.execute('''
CREATE TABLE IF NOT EXISTS bookings(
id INT,
client_id INT NOT NULL,
service_id INT NOT NULL,
_date_ INT NOT NULL
);
''')
conn.commit()