import sqlite3

con = sqlite3.connect('cas.db')

canteen = [['Food Point', '@pass'], ['13th Floor Cafe', "@pass"], ['Food Truck', '@pass']]
con.executemany('insert into Canteens (canteen_name, password) values (?, ?)', canteen)

user = [['Vaibhav Pundir', '@pass', 'student'], ['Vaibhav B.V', '@pass', 'student'], ['Devashish', '@pass', 'student'],
['Saketh', '@pass', 'student'], ['Yashvanth', '@pass', 'student'], ['Vedant', '@pass', 'student'], ['Vishwas', '@pass', 'student'], 
['Shreekanth M Prabhu', '@pass', 'faculty']]
con.executemany('insert into Users (username, password, type) values (?, ?, ?)', user)

con.commit()
con.close()