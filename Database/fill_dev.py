import sqlite3

con = sqlite3.connect('cas.db')

con.execute('insert into Canteens values (10000, "Developer", "dev@123");')
con.execute('insert into Users (user_id, username, password, type) values (20000, "Developer", "dev@123", "dev");')
con.execute('insert into Foods values (30000, "DevFood", "dev");')
con.execute('insert into Combos values (40000, "DevCombo", 0, 10000);')
con.execute('insert into Orders values (50000, 20000, 10000, 30000, "Developer", 0, "22-11-2019");')
con.execute('insert into Items values (60000, "DevItem");')

con.commit()
con.close()