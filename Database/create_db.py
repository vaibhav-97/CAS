import sqlite3

con = sqlite3.connect('cas.db')

con.execute('PRAGMA foreign_keys = ON')

con.execute('''create table Canteens(canteen_id INTEGER PRIMARY KEY AUTOINCREMENT,
canteen_name TEXT NOT NULL UNIQUE,
password TEXT NOT NULL);''')

con.execute('''create table Users(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL UNIQUE,
password TEXT NOT NULL,
wallet INTEGER DEFAULT 0,
type TEXT NOT NULL);''')

con.execute('''create table Foods(food_id INTEGER PRIMARY KEY AUTOINCREMENT,
food_name TEXT NOT NULL UNIQUE,
category TEXT NOT NULL);''')

con.execute('''create table Menu(canteen_id INTEGER,
food_id INTEGER,
price INTEGER NOT NULL,
units_ordered INTEGER DEFAULT 0,
PRIMARY KEY(canteen_id, food_id),
FOREIGN KEY(canteen_id) REFERENCES Canteens(canteen_id) ON DELETE CASCADE,
FOREIGN KEY(food_id) REFERENCES Foods(food_id) ON DELETE CASCADE);''')

con.execute('''create table Combos(combo_id INTEGER PRIMARY KEY AUTOINCREMENT,
combo_name TEXT NOT NULL,
price INTEGER NOT NULL,
canteen_id INTEGER REFERENCES Canteens(canteen_id) ON DELETE CASCADE);''')

con.execute('''create table Contains(combo_id INTEGER REFERENCES Combos(combo_id) ON DELETE CASCADE,
food_id INTEGER REFERENCES Foods(food_id) ON DELETE CASCADE,
PRIMARY KEY(combo_id, food_id));''')

con.execute('''create table Orders(order_id INTEGER PRIMARY KEY,
user_id INTEGER REFERENCES Users(user_id) ON DELETE CASCADE,
canteen_id INTEGER REFERENCES Canteens(canteen_id) ON DELETE CASCADE,
food_id INTEGER REFERENCES Foods(food_id) ON DELETE CASCADE,
feedback TEXT,
rating INTEGER,
date INTEGER);''')

con.execute('''create table Items(item_id INTEGER PRIMARY KEY AUTOINCREMENT,
item_name TEXT NOT NULL UNIQUE);''')

con.execute('''create table Invertory(item_id INTEGER REFERENCES Items(item_id) ON DELETE CASCADE,
canteen_id INTEGER REFERENCES Canteens(canteen_id) ON DELETE CASCADE,
total_qty INTEGER NOT NULL,
PRIMARY KEY(item_id, canteen_id));''')

con.execute('''create table Requirements(canteen_id INTEGER REFERENCES Canteens(canteen_id) ON DELETE CASCADE,
food_id INTEGER REFERENCES Foods(food_id) ON DELETE CASCADE,
item_id INTEGER REFERENCES Items(item_id) ON DELETE CASCADE,
reqd_qty INTEGER NOT NULL,
PRIMARY KEY(canteen_id, food_id, item_id));''')

con.commit()
con.close()