import sqlite3

connection = sqlite3.connect("hydroponic.db")
cursor = connection.cursor()
#connection.executemany("insert into person(firstname, lastname) values (?,?)", persons)

cursor.execute("CREATE TABLE IF NOT EXISTS ppm (ppm TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS ph (ph TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS tem (celsius TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS detec (detec TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT,password TEXT)")
# cursor.execute("CREATE TABLE IF NOT EXISTS prueba (username TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP)")

# cursor.execute("INSERT INTO prueba VALUES ('juan')")

# ph = ["12.3"]

# t1=tuple(ph[0:1])
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

#cursor.execute("INSERT INTO ppm VALUES (?)",t)
# cursor.execute("INSERT INTO ph VALUES (?)",t1)
#cursor.execute("INSERT INTO tem VALUES (?)",t2)
#cursor.execute("INSERT INTO detec VALUES (?)",t3)
#cursor.execute('DELETE FROM ph')
ph =[22,22]    
print(ph[0])
connection.commit()

result = cursor.execute("SELECT * FROM users WHERE username = (?)", ('ben',))
# result = cursor.fetchall()
username = "benja"
for row in result:
    print("Name = ", row[0])
    print("Email  = ", row[1])
 
rows2 = cursor.execute("SELECT * FROM tem")
result = cursor.execute("SELECT * FROM users WHERE username = 'benjas'")
print(result.fetchone() is None)
if result is None:
    print("there")

else:
    for row in result:
        (row)

cursor.close()
