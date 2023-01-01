from flask import Flask, render_template, request, Response
from selenium import webdriver 
from selenium.webdriver.common.by import By
import sqlite3
from flask import g
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import time
import cv2
app = Flask(__name__)

ph = ["10.34ph"]
ppm = []
de = []
de1 = ["30.23C"]

def transfo(table):
    connection = sqlite3.connect("hydroponic.db")
    cursor = connection.cursor()
    r = 0
    data = []
    data1= []

    pro =""
    rows1 = cursor.execute(f"SELECT * FROM {table}")
    #rows1 = cursor.execute(f"SELECT * FROM ph")
    for row in rows1:
        data.append(row)
    
    pro ="".join(map(str,data))
    num = ""
    for c in pro:
        if c.isdigit():
            num = num + c
    n = 4
    graph =[num[i:i+n] for i in range(0, len(num), n)]
    lst1 = pro.split(",")
    for a in graph:
        r= r +1
        data1.append(r)
    return graph
def new(table):
    r = 0
    d = []
    for a in transfo(table):
        r= r +1
        d.append(r)
    return d
def get_data():
    chrome_driver_path = "C:\selen\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get("http://192.168.100.29/")
    ing = driver.find_element(By.XPATH,"/html/body/p[2]/textarea")
    dat = ing.text
    return dat

def db():
    t=tuple(ppm[0:1])
    t1=tuple(ph[0:1])
    #t1=("12.34ph")
    t2=tuple(de[0:1])
    t3=tuple(de1[0:1])
    connection = sqlite3.connect("hydroponic.db")
    cursor = connection.cursor()
    #connection.executemany("insert into person(firstname, lastname) values (?,?)", persons)
    cursor.execute("CREATE TABLE IF NOT EXISTS ppm (ppm TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS ph (ph TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS tem (celsius TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS detec (detec TEXT)")
    #cursor.execute("INSERT INTO ph VALUES (?)",t1)
    #cursor.execute("INSERT INTO tem VALUES (?)",t3)
    #cursor.execute("INSERT INTO detec VALUES (?)",t3)
    #cursor.execute('DELETE FROM ph')

    connection.commit()
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("hydroponic.db") 
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS ph (ph TEXT)")
        t=tuple(ppm[0:1])
        t1=tuple(ph[0:1])
        #t1=("12.34ph")
        t2=tuple(de[0:1])
        t3=tuple(de1[0:1])
        cursor.execute("INSERT INTO ph VALUES (?)",t1)
    return db
                

def separate(dat):
    chrome_driver_path = "C:\selen\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get("http://192.168.100.29/")
    ing = driver.find_element(By.XPATH,"/html/body/p[2]/textarea")
    dat = ing.text
    suffix = "ppm"
    suffix1 = "ph"
    suffix2 = "a:"
    suffix3 = "C"
    lst = dat.split("\n")

    for i in lst:
        if(i.find(suffix) != -1):
            #ppm = ppm + i 

            ppm.append(i)
            res = True
        elif(i.find(suffix1) != -1):
            ph.append(i)
            res = True
        elif(i.find(suffix2) != -1):
            de.append(i)
            res = True
        elif(i.find(suffix3) != -1):
            de1.append(i)
            res = True

def push(path):
    chrome_driver_path = "C:\selen\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get("http://192.168.100.29/")
    led_v=driver.find_element(By.XPATH,path)
    led_v.click()
    #print(dat)
    #time.sleep(10)
    return render_template("index.html")

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unautorized, please login')
            return redirect(url_for('login'))
    return wrap


@app.route("/", methods=['GET', 'POST'])
@is_logged_in
def index():
    labels= new("ph")
    values= transfo("ph")
    labels1= new("tem")
    values1= transfo("tem")

    h = "jddsj"
    
    if request.method == 'POST':
        if request.form.get('action1') == 'Bomba A1 ON':
            push("/html/body/p[4]/a/button")
            separate(get_data)
            db()
        elif  request.form.get('action2') == 'Bomba A1 OFF':
            push("/html/body/a[1]/button")
            
        elif  request.form.get('action3') == 'TDS ON':
            push("/html/body/p[6]/a/button")

        elif  request.form.get('action4') == 'TDS OFF':
            push("/html/body/a[2]/button")
        
        elif  request.form.get('action5') == 'PH ON':
            push("/html/body/p[8]/a/button")

        elif  request.form.get('action6') == 'PH OFF':
            push("/html/body/a[3]/button")
        
        elif  request.form.get('action7') == 'DetectW1 ON':
            push("/html/body/p[10]/a/button")

        elif  request.form.get('action8') == 'DetectW1 OFF':
            push("/html/body/a[4]/button")
        
        elif  request.form.get('action9') == 'DetectW2 ON':
            push("/html/body/p[12]/a/button")
        
        elif  request.form.get('action10') == 'DetectW2 OFF':
            push("/html/body/a[5]/button")
        
        elif  request.form.get('action11') == 'Dosif1 ON':
            push("/html/body/p[14]/a/button")
        
        elif  request.form.get('action12') == 'Dosif1 OFF':
            push("/html/body/a[6]/button")
        
        elif  request.form.get('action13') == 'Dosif2 ON':
            push("/html/body/p[16]/a/button")
        
        elif  request.form.get('action14') == 'Dosif2 OFF':
            push("/html/body/a[7]/button")
        
        elif  request.form.get('action15') == 'Dosif3 ON':
            push("/html/body/p[18]/a/button")
        
        elif  request.form.get('action16') == 'Dosif3 OFF':
            push("/html/body/a[8]/button")
        
        elif  request.form.get('action17') == 'Dosif4 ON':
            push("/html/body/p[20]/a/button")
        
        elif  request.form.get('action18') == 'Dosif4 OFF':
            push("/html/body/a[9]/button")

        elif  request.form.get('action19') == 'Manual ON':
            push("/html/body/p[22]/a/button")
        
        elif  request.form.get('action20') == 'Manual OFF':
            push("/html/body/p[23]/a/button")
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('index.html',labels=labels, values=values,labels1=labels1, values1=values1)
    
    #return render_template("index.html",dat=dat, h=h)
    return render_template("index.html",labels=labels, values=values,labels1=labels1, values1=values1)

@app.route("/home")
def home():
    data = [
        ("1",1223),
        ("2",1623),
        ("3",1523),
        ("4",1423),
    ]

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    return render_template("graph.html", labels=labels, values=values)
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g,'_database',None)
    if db is not None:
        db.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = sqlite3.connect("hydroponic.db")

    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = ?", (username,))
       
            # Get stored hash
        data = cur.fetchone() is None
        

        if data == False: # Compare Passwords
            result = cur.execute("SELECT * FROM users WHERE username = ?", (username,))
            data1 = cur.fetchone()
            password = data1[1]
            session['logged_in'] = True
            if password_candidate == password:
                # Passed

            
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('index'))
                #return render_template("dashboard.html")
            elif password_candidate != password:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
        else:
            error = 'Username not found'
            return render_template('login.html', error=error,result=result)
    return render_template('login.html')

# separate()
# db()
if __name__ == "__main__":
    app.secret_key='benji123'
    app.run(debug=True)
    



#driver.quit()
# from flask import Flask, render_template, request
# app = Flask(__name__)
# @app.route("/", methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if request.form.get('action1') == 'VALUE1':
#             pass # do something
#         elif  request.form.get('action2') == 'VALUE2':
#             pass # do something else
#         else:
#             pass # unknown
#     elif request.method == 'GET':
#         return render_template('index.html')
    
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)