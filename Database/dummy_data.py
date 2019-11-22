import sqlite3

con = sqlite3.connect('Canteen.db')

admin = [['admin1', '@123'], ['admin2', '@123'], ['admin3', '@123']]

user = [['Vaibhav B.V', 'user1', '@123'], ['Vaibhav Pundir', 'user2', '@123'], ['Devashish', 'user3', '@123'], ['Saketh', 'user4', '@123'],
['Vedant', 'user5', '@123'], ['Yashvanth', 'user6', '@123'], ['Vishwas', 'user7', '@123']]

menu = [['item1', 'Soup', 'admin1', 25], ['item2', 'Aloo Paratha', 'admin1', 20], ['item3', 'Paneer Butter Masala', 'admin1', 50],
['item4', 'Veg Fried Rice', 'admin1', 60], ['item5', 'Grilled Chicken', 'admin1', 80], ['item6', 'Tandoori Chicken', 'admin1', 60],
['item7', 'Coke', 'admin1', 50], ['item8', 'Sprite', 'admin1', 50], ['item9', 'Veg Noodles', 'admin1', 50], ['item10', 'Butter Naan', 'admin1', 20],
['item11', 'Soup', 'admin2', 25], ['item12', 'Aloo Paratha', 'admin2', 20], ['item13', 'Paneer Butter Masala', 'admin2', 50],
['item14', 'Veg Fried Rice', 'admin2', 60], ['item15', 'Grilled Chicken', 'admin2', 80], ['item16', 'Tandoori Chicken', 'admin2', 60],
['item17', 'Coke', 'admin2', 50], ['item18', 'Sprite', 'admin2', 50], ['item19', 'Veg Noodles', 'admin2', 50], ['item20', 'Butter Naan', 'admin2', 20],
['item21', 'Soup', 'admin3', 25], ['item22', 'Aloo Paratha', 'admin3', 20], ['item23', 'Paneer Butter Masala', 'admin3', 50],
['item24', 'Veg Fried Rice', 'admin3', 60], ['item25', 'Grilled Chicken', 'admin3', 80], ['item26', 'Tandoori Chicken', 'admin3', 60],
['item27', 'Coke', 'admin3', 50], ['item28', 'Sprite', 'admin3', 50], ['item29', 'Veg Noodles', 'admin3', 50], ['item30', 'Butter Naan', 'admin3', 20]]

combo = [['combo1', 'admin1', 100], ['combo2', 'admin2', 90], ['combo3', 'admin3', 110], ['combo4', 'admin2', 120], ['combo5', 'admin1', 80]]

contains = [['item4', 'combo1'], ['item8', 'combo1'], ['item17', 'combo2'], ['item19', 'combo2'], ['item23', 'combo3'], ['item30', 'combo3'],
['item12', 'combo4'], ['item18', 'combo4'], ['item3', 'combo5'], ['item4', 'combo5']]



con.executemany('insert into Admin values (?, ?);', admin)
con.executemany('insert into User values (?, ?, ?);', user)
con.executemany('insert into Menu values (?, ?, ?, ?);', menu)
con.executemany('insert into Combos values (?, ?, ?);', combo)
con.executemany('insert into Contains values (?, ?);', contains)

con.commit()
con.close()
