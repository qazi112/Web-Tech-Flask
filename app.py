from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for

import sqlite3 as sql

def create_table():
   conn = sql.connect("database.db")
   if conn.execute("""CREATE TABLE students(s_id INTEGER PRIMARY KEY AUTOINCREMENT,s_name TEXT NOT NULL,
      addr TEXT, city TEXT , pincode TEXT );"""):
      print("Created")
   else:
         print("Error")
   conn.close()

app = Flask(__name__)

@app.route('/add')
def new_student():
   return render_template('student.html')


@app.route('/newrecord',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         with sql.connect("database.db") as con:
            
            cur = con.cursor()
            cur.execute("INSERT INTO students (s_name,addr,city,pincode) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()


@app.route('/list')

def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall(); 
  
   return render_template("list.html",rows = rows)


@app.route('/')
def home():
   return render_template("home.html")

# to delete record
@app.route("/delete/<s_id>")
def delete(s_id):
   student_id = s_id
   msg = ""
   try:
      with sql.connect("database.db") as conn:
         cur = conn.cursor()
         query= "DELETE FROM students WHERE s_id = ?;"

         cur.execute(query,(student_id,))
         conn.commit()

         query = """UPDATE `sqlite_sequence`
         SET `seq` = (SELECT MAX(`s_id`) FROM 'students')
         WHERE `name` = 'students';"""
         cur.execute(query)
         conn.commit()
         cur.close()
         msg = "SUCCESS"
   except:
      conn.rollback()
      print("Error")
      msg = "error in Deletion operation"

   
      
   return redirect(url_for("list"))
   conn.close()


if __name__ == '__main__':
   app.run(debug = True,host="127.0.0.1",port=5051)