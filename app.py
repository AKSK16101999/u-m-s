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
        # if f_name or l_name or email or uname or phone or address or password1 or password2:
        #     error = 'Please enter the all details'
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
    # user_info = request.form
    msg = ' '

    name = request.form['uname']
    password = request.form['pass']
    if name and password:
        cur = db.connection.cursor()
        cur.execute("SELECT username, password from userdata where username=%s and password=%s ", (name, password))
        data = cur.fetchone()
        try:
            session['loggedin'] = True
            session['username'] = data[0]
            session['password'] = data[1]
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
        print(session)
        cur.execute(f"SELECT * FROM userdata WHERE Username ='{session['username']}'")
        account = cur.fetchone()
        print(type(account))
        print(account)
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

        query = f"Update userdata SET First_Name='{fname}', Last_Name='{lname}', Email='{email}',Username='{uname}'," \
                f" Phone='{phone}', Address='{address}', password='{password1}', Cpassword='{password2}' " \
                f"where Username ='{session['username']}'"

        cur.execute(query)
        db.connection.commit()
        msg = "Your account updated successfully."
    else:
        msg = "Some error occurs."
        return render_template("update.html", msg=msg, user=session['username'])
    return redirect(url_for('update'))


@App.route("/evses")
def evses():
    return render_template('evses.html', user=session['username'])


@App.route("/add")
def add():
    return render_template('add.html', user=session['username'])


@App.route("/remove", methods=['POST', 'GET'])
def remove():
    return render_template('remove.html', user=session['username'])


@App.route("/modify", methods=['POST', 'GET'])
def modify():
    return render_template('modify.html', user=session['username'])


if __name__ == '__main__':
    App.run()
