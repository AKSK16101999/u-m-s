from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL

App = Flask(__name__)
App.secret_key = '12345678'
App.config['MYSQL_USER'] = 'test'
App.config['MYSQL_PASSWORD'] = '12345678'
App.config['MYSQL_HOST'] = 'localhost'
App.config['MYSQL_DB'] = 'test'
App.config['MYSQL_CURSOR'] = 'DictCursor'

db = MySQL(App)


@App.route('/')
@App.route('/signup')
def registration():
    return render_template('register.html')


@App.route('/signup', methods=['POST', 'GET'])
def signup():
    error = ""
    msg = ""
    cur = db.connection.cursor()
    if request.method == 'POST':
        f_name = request.form.get('fname')
        l_name = request.form.get('lname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        uname = request.form.get('uname')
        address = request.form.get('add')
        password1 = request.form.get('pass')
        password2 = request.form.get('pass1')
        query = f"select Email from userdata where Email ='{email}'"
        cur.execute(query)
        data = cur.fetchone()
        if data:
            error = 'Email already exist'
        if len(password1) < 6:
            error = 'password should have at list 6 char'
        elif password1 != password2:
            error = 'password not match'
        elif f_name and l_name and email and uname and phone and address and password1 and password2:
            query = "INSERT INTO userdata (First_Name, Last_Name, Email, Username, Phone , Address, password, " \
                    "Cpassword) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
            cur.execute(query, (f_name, l_name, email, uname, phone, address, password1, password2))
            db.connection.commit()
        msg = "Your account created successfully."
    if error:
        return render_template('register.html', error=error)
    elif msg:
        return render_template('register.html', msg=msg)


@App.route('/login')
def login():
    return render_template('login.html')


@App.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@App.route('/login', methods=['POST', 'GET'])
def signin():
    name = request.form['uname']
    password = request.form['pass']
    if name and password:
        cur = db.connection.cursor()
        cur.execute("SELECT username, password, Email from userdata where username=%s and password=%s ",
                    (name, password))
        data = cur.fetchone()
        try:
            session['loggedin'] = True
            session['username'] = data[0]
            session['password'] = data[1]
            session['email'] = data[2]
            msg = "Login Successfully!!!"
            return render_template('home.html', msg=msg, user=session['username'])
        except:
            msg = "User name and Password is wrong"
            return render_template('login.html', msg=msg)
    else:
        msg = 'Please enter the username and password'
        return render_template('login.html', msg=msg)


@App.route('/index')
def index():
    if 'loggedin' in session:
        return render_template('profile.html', user=session['username'])
    return render_template('login')


@App.route("/display")
def display():
    if 'loggedin' in session:
        cur = db.connection.cursor()
        cur.execute(f"SELECT * FROM userdata WHERE Email ='{session['email']}'")
        account = cur.fetchone()
        return render_template("display.html", account=account, user=session['username'])
    return redirect(url_for('login'))


@App.route('/update', methods=['POST', 'GET'])
def Update():
    return render_template('update.html', user=session['username'])


@App.route("/update", methods=['POST', 'GET'])
def update():
    # print(session)
    cur = db.connection.cursor()
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        uname = request.form.get('uname')
        address = request.form.get('add')
        password1 = request.form.get('pass')
        password2 = request.form.get('pass1')
        print('get')
        query = f"Update userdata SET First_Name='{fname}', Last_Name='{lname}', Email='{email}',Username='{uname}'," \
                f" Phone='{phone}', Address='{address}', password='{password1}', Cpassword='{password2}' " \
                f"where Email ='{session['email']}'"
        print('set')
        cur.execute(query)
        db.connection.commit()
        msg = "Your account updated successfully."
    else:
        msg = "Some error occurs."
    return render_template("update.html", msg=msg, user=session['username'])


@App.route("/evses")
def evses():
    if session:
        cur = db.connection.cursor()
        cur.execute(f"SELECT * FROM evs WHERE Email ='{session['email']}'")
        acc = cur.fetchall()
        return render_template('evses.html', user=session['username'], acc=acc)


@App.route("/add")
def add1():
    return render_template('add.html')


@App.route("/add", methods=['POST', 'GET'])
def add():
    cur = db.connection.cursor()
    if request.method == 'POST':
        make = request.form.get('make')
        model = request.form.get('model')
        model_year = request.form.get('model_year')
        color = request.form.get('color')
        email = session['email']
        if email and make and model and model_year and color:
            query = "INSERT INTO evs (Email, Make, Model , Model_Year, Color" \
                    ") VALUES ( %s, %s, %s, %s, %s) "
            cur.execute(query, (email, make, model, model_year, color))
            db.connection.commit()
            msg = "Evs added successfully."
        else:
            error = 'please enter the all details'
            return render_template('add.html', error=error)
        return render_template('add.html', msg=msg)
    return redirect(url_for('add'))


@App.route("/remove", methods=['POST', 'GET'])
def remove1():
    return render_template("remove.html", user=session['username'])


@App.route("/remove", methods=['POST', 'GET'])
def remove():
    cur = db.connection.cursor()
    if request.method == 'POST':
        model = request.form.get('model')
        query = f"Delete from evs where Model ='{model}'"
        cur.execute(query)
        db.connection.commit()
        msg = "Your Evs Deleted successfully."
    else:
        msg = "Some error occurs."
    return render_template("remove.html", msg=msg, user=session['username'])


@App.route("/modify", methods=['POST', 'GET'])
def modify1():
    return render_template("modify.html", user=session['username'])


@App.route("/modify", methods=['POST', 'GET'])
def modify():
    cur = db.connection.cursor()
    if request.method == 'POST':
        make = request.form.get('make')
        model = request.form.get('model')
        model_year = request.form.get('model_year')
        color = request.form.get('color')
        query = f"Update evs SET Make='{make}', Model='{model}', Model_Year='{model_year}', Color='{color}' " \
                f"where Model ='{model}'"
        cur.execute(query)
        db.connection.commit()
        msg = "Your Evs updated successfully."
    else:
        msg = "Some error occurs."
    return render_template("modify.html", msg=msg, user=session['username'])


if __name__ == '__main__':
    App.run()
