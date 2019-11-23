from flask import Flask, render_template, request,Response
import json
import sqlite3
from threading import Lock

admin_dict=dict()

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/signup.html/<type>')
def admin_signup(type):
    return render_template('signup.html', type=type)

@app.route('/login.html/<type>')
def admin_login(type):
    return render_template('login.html', type=type)

@app.route('/create.html/admin', methods=['POST'])
def create_admin():
    con = sqlite3.connect('Database/Canteen.db')
    command = "insert into Admin values (?, ?);"
    try:
        con.execute(command, (request.form['userid'], request.form['pass']))
    except Exception as e:
        print(e)
        con.close()
        return render_template('signup.html', type='admin')
    con.commit()
    con.close()
    print('success')
    return json.dumps('admin created');#render_template('admin_view.html')

@app.route('/create.html/user', methods=['POST'])
def create_user():
    con = sqlite3.connect('Database/Canteen.db')
    command = "insert into User values (?, ?, ?);"
    try:
        con.execute(command, (request.form['name'], request.form['userid'], request.form['pass']))
    except Exception as e:
        print(e)
        con.close()
        return render_template('signup.html', type='user')
    con.commit()
    con.close()
    print('success')
    return json.dumps('user created');#render_template('user_view.html')

@app.route('/verify/admin', methods=['POST'])
def verify_admin():
    con = sqlite3.connect('Database/Canteen.db')
    command = 'select * from Admin where admin_id = ? and password = ?;'
    cur = con.cursor()
    try:
        cur.execute(command, (request.form['id'], request.form['pass']))
        log = cur.fetchall()
        print(log)
        if log:
            cur.close()
            return render_template('admin.html', admin_id=log[0][0])
        else:
            cur.close()
            return render_template('login.html', type='admin')
    except Exception as e:
        print(e)
        cur.close()
        return render_template('login.html', type='admin')

@app.route('/verify/user', methods=['POST'])
def verify_user():
    con = sqlite3.connect('Database/Canteen.db')
    command = 'select * from User where user_id = ? and password = ?;'
    cur = con.cursor()
    try:
        cur.execute(command, (request.form['id'], request.form['pass']))
        log = cur.fetchall()
        print(log)
        if log:
            query = 'select distinct admin_id from Menu'
            cur.execute(query)
            menu = cur.fetchall()
            '''query = 'select food, price, combo_id from (Menu natural join Contains)'
            try:
                cur.execute(query)
            except Exception as e:
                print(e)
                con.close()
                return json.dumps('failed')#render_template()'''
            '''items = cur.fetchall()
            data = {}
            for i in items:
                if i[2] not in data.keys():
                    data[i[2]] = list(i[:2])
                else:
                    data[i[2]][0] = data[i[2]][0] + ',' + i[0]'''
            return render_template('user.html', menu=menu, user_id=request.form['id'])
        else:
            cur.close()
            return render_template('login.html', type='user')
    except Exception as e:
        print(e)
        cur.close()
        return render_template('login.html', type='user')

@app.route('/get_menu/<canteen>/<user_id>')
def get_menu(canteen, user_id):
    con = sqlite3.connect('Database/Canteen.db')
    cur = con.cursor()
    query = 'select item_id, food, price from Menu where admin_id = ?;'
    try:
        cur.execute(query, (canteen, ))
    except Exception as e:
        print(e)
        con.close()
        return json.dumps('failed')#render_template()
    menu = cur.fetchall()
    con.close()
    return render_template('display_menu.html', menu=menu, admin_id=canteen, user_id=user_id)

@app.route('/place_order',methods=["POST"])
def place_order():
    print(request.form)
    admin_id=request.form["admin_id"]
    food_items=list(request.form)
    print(food_items)
    user_id=request.form["user_id"]
    food_items=food_items[:-2]
    if admin_id not in admin_dict:return json.dumps('failed')
    lock,olist=admin_dict[admin_id]
    for i in food_items:olist.append([user_id,i])
    lock.release()
    return json.dumps("success")   

@app.route('/add_to_cart', methods=["POST"])
def add_to_cart():
    ids = list(request.form)
    

# These are all post requests right ,ok
#Nope
@app.route('/addfooditems/<admin_id>')
def addfooditems(admin_id):
    #this is implemented, see add_items
    return render_template('addfooditems.html', admin_id=admin_id)

#this is post
@app.route('/add_items', methods=['POST'])
def add_items():
    #implement acceptorders, line 116
    con = sqlite3.connect('Database/Canteen.db')
    command = 'insert into Menu values (?, ?, ?, ?);'
    try:
        con.execute(command, (request.form['item_id'], request.form['food'], request.form['admin_id'], request.form['price']))
    except Exception as e:
        print(e)
        con.close()
        return json.dumps("failed")#render_template()
    con.commit()
    con.close()
    return render_template('admin.html', admin_id=request.form['admin_id'])

@app.route('/deletefooditems/<admin_id>')
def deletefooditems(admin_id):
    con = sqlite3.connect('Database/Canteen.db')
    cur = con.cursor()
    query = 'select item_id, food, price from Menu where admin_id = ?'
    try:
        cur.execute(query, (admin_id, ))
    except Exception as e:
        print(e)
        con.close()
        return json.dumps('failed')#render_template()
    items = cur.fetchall()
    return render_template('deletefooditems.html', result=items, admin_id=admin_id)

@app.route('/delete_items', methods=['POST'])
def delete_items():
    ids = list(request.form)
    con = sqlite3.connect('Database/Canteen.db')
    command = 'delete from Menu where item_id = ? and admin_id = ?;'
    try:
        for id in ids[:-1]:
            con.execute(command, (id, request.form[ids[-1]]))
    except Exception as e:
        print(e)
        con.close()
        return json.dumps('failed')#render_template()
    con.commit()
    con.close()
    return render_template('admin.html', admin_id=request.form['admin_id'])

@app.route('/addfoodcombos/<admin_id>')
def addfoodcombos(admin_id):
    con = sqlite3.connect('Database/Canteen.db')
    cur = con.cursor()
    query = 'select item_id, food, price from Menu where admin_id = ?;'
    try:
        cur.execute(query, (admin_id, ))
    except Exception as e:
        print(e)
        cur.close()
        return json.dumps("failed")#render_template()
    items = cur.fetchall()
    print(items)
    return render_template('addfoodcombos.html', result=items, admin_id=admin_id)

#add_combos i mean insert into database one just like add_items ,add_combos for  ok
#i am doing combos, what?? ohhh. okay. do it. i will make front end that will use add_combos

##also for the contains table is this also needed
def add_contains(con, combo_id, values):
    #con=sqlite3.connect('Database/Canteen.db')
    ids = list(values)[:-3]
    command = 'insert into Contains values (?, ?);'
    for i in ids:
        try:
            con.execute(command, (i, combo_id)) #need to verify order
        except Exception as e:
            print(e)
            return False #fail
    #con.commit() #we can call commit outside
    return True

#let me know once you complete this api
#I dont know how the data input is - ok got a clue - ok
#check addfoodcombos.html from line 75
@app.route('/add_combos',methods=['POST'])
def add_combos():
    con = sqlite3.connect('Database/Canteen.db')
    command = 'insert into Combos values (?, ?, ?);'

    try:            #first adding to Combos
        con.execute(command, (request.form['combo_id'], request.form['admin_id'], request.form['price']))
    except Exception as e:
        print(e)
        con.close()
        return json.dumps("failed")#render_template
    #fooditems may not work if request.form is immutable
    combo_id = request.form['combo_id']#del(request.form['combo_id'])
    admin_id = request.form['admin_id']#del(request.form['admin_id'])
    price = request.form['price']#del(request.form['price'])

    if not add_contains(con, combo_id, request.form):        #adding fooditems
        con.close()
        return json.dumps("failed")#render_template()

    con.commit()
    con.close()
    return render_template('admin.html', admin_id=request.form['admin_id'])


@app.route('/deletefoodcombos/<admin_id>')
def deletefoodcombos(admin_id):
    con = sqlite3.connect('Database/Canteen.db')
    cur = con.cursor()
    query = 'select food, price, combo_id from (Menu natural join Contains) where admin_id = ?;'
    try:
        cur.execute(query, (admin_id, ))
    except Exception as e:
        print(e)
        con.close()
        return json.dumps('failed')#render_template()
    items = cur.fetchall()
    data = {}
    for i in items:
        if i[2] not in data.keys():
            data[i[2]] = list(i[:2])
        else:
            data[i[2]][0] = data[i[2]][0] + ',' + i[0] 
    print(data)
    return render_template('deletefoodcombos.html', result=data, admin_id=admin_id)

@app.route('/delete_combos', methods=['POST'])
def delete_combos():
    con = sqlite3.connect('Database/Canteen.db')
    command = 'delete from Combos where combo_id = ? and admin_id = ?;'
    try:
        for i in list(request.form)[:-1]:
            con.execute(command, (request.form[i], request.form['admin_id']))
    except Exception as e:
        print(e)
        con.close()
        return json.dumps('failed')#render_template()
    con.commit()
    con.close()
    return render_template('admin.html', admin_id=request.form['admin_id'])

@app.route('/acceptorders/<admin_id>')
def acceptorders(admin_id):
    return render_template('acceptorders.html', admin_id = admin_id)



#server_sent_events assuming GET
def runget(lock,order_list):
    yield "data flow started\n\n"
    while True:
        lock.acquire(1)
        to_send=order_list.copy()
        order_list.clear()
        print("sent2"+json.dumps(to_send))
        yield 'data: '+json.dumps(to_send)+'\n\n'
        #yield 'data:"soehng"\n\n'


@app.route('/acceptorders/admin_sse/<admin_id>')
def admin_sse(admin_id):
    print("called admin_sse")
    print(admin_dict, admin_id)
    if admin_id not in admin_dict:
        print('failed')
        return json.dumps('failed')
    lock,order_list=admin_dict[admin_id]
    print(admin_dict)
    print("my",order_list)
    return Response(runget(lock,order_list), mimetype="text/event-stream")

 
##sse_debug page
@app.route('/admin_recv_dbg.html')
def admin_debug():
    return render_template("admin_recv.html")


if __name__ == '__main__':

    con = sqlite3.connect('Database/Canteen.db')
    admin_list=con.execute("select admin_id from Admin;").fetchall()
    con.close()
    for i in admin_list:
        mutex=Lock()
        mutex.acquire(1)
        admin_dict[i[0]]=[mutex,[]]         #lock,order_list


    app.run(host = 'localhost', debug = True)
