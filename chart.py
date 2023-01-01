from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response
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

ph = ["10.34ph"]
ppm = []
de = []
de1 = []

app = Flask(__name__)
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
    return graph[-1]
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
    cursor.execute("INSERT INTO tem VALUES (?)",t3)
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

@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    pro ="".join(map(str,ph))
    num = ""
    for c in pro:
        if c.isdigit():
            num = num + c
    n = 4
    graph =[num[i:i+n] for i in range(0, len(num), n)]
    lst1 = pro.split(",")

    data = [22, 22 ]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


if __name__ == "__main__":
    app.run(debug=True)