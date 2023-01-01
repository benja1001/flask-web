from flask import Flask, render_template
import sqlite3

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
    return graph
def new():
    r = 0
    d = []
    for a in transfo("ph"):
        r= r +1
        d.append(r)
    return d
@app.route("/")
def home():
    data = [
        ("1",1223),
        ("2",1623),
        ("3",1523),
        ("4",1423),
    ]

    # labels = [row[0] for row in data]
    # values = [row[1] for row in data]
    labels = transfo("ph")
    values = new()

    return render_template("graph.html", labels=labels, values=values)

if __name__ == "__main__":
    app.run(debug=True)
