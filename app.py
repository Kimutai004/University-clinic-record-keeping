
from flask import Flask, render_template, request, redirect, url_for, session,flash
from datetime import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors
# import db
import re
import pymysql
import random
from flask_sqlalchemy import SQLAlchemy
import string
  
  
app = Flask(__name__)
  
  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hmisphp'
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user  WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            # return render_template('dashboard.html', mesage = mesage)
            return redirect(url_for('dashboard'))
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))



@app.route('/sidebar')
def sidebar():
 	return render_template('sidebar.html')

@app.route('/nav')
def nav():
    return render_template('nav.html') 

@app.route('/footer')
def footer():
    return render_template('footer.html') 

@app.route('/footer1')
def footer1():
    return render_template('footer1.html')  

@app.route('/head')
def head():
    return render_template('head.html') 

@app.route('/registerstudent')
def registerstudent():
    return render_template('registerstudent.html') 

@app.route('/viewstudents')
def viewstudents():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM his_patients")
    data =cursor.fetchall()
    return render_template('viewstudents.html', his_patients=data) 

@app.route('/managestudent')
def managestudent():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM his_patients")
    data =cursor.fetchall()
    return render_template('managestudent.html', his_patients=data) 

@app.route('/instudentpage')
def instudentpage():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM his_patients")
    data =cursor.fetchall()
    return render_template('instudentpage.html', his_patients=data)






@app.route('/inpatientrecords')
def inpatientrecords():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM his_patients WHERE pat_type = 'Instudent'  " )
    data =cursor.fetchall()
    return render_template('inpatientrecords.html ', his_patients=data)


@app.route('/outpatientrecords')
def outpatientrecords():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM his_patients WHERE pat_type = 'Outstudent'  " )
    data =cursor.fetchall()
    return render_template('outpatientrecords.html ', his_patients=data) 



@app.route('/viewsinglestudent')
def viewsinglestudent():
    pat_id = request.args.get('pat_id')
    # pat_number = request.args.get('pat_number')
    cursor=mysql.connection.cursor()
    query = "SELECT * FROM his_patients WHERE pat_id = %s"
    # cursor.execute(query,(pat_id,))
    # data =cursor.fetchall()
    return render_template('viewsinglestudent.html ', his_patients='data')


@app.route('/delete-admin/<pat_id>', methods=['GET'])
def delete_admin(pat_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM his_patients WHERE pat_id=%s',(pat_id,))
    mysql.connection.commit()
    flash('admin deleted successfully','success')

    return redirect(url_for('instudentpage'))

@app.route('/delete-admin1/<pat_id>', methods=['GET'])
def delete_admin1(pat_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM his_patients WHERE pat_id=%s',(pat_id,))
    mysql.connection.commit()
    flash('admin deleted successfully','success')

    return redirect(url_for('instudentpage'))    




@app.route('/updatesinglestudent/<int:admin_id>', methods=['GET', 'POST'])
def edit_admin(admin_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)


    # Fetch the admin data by ID
    cursor.execute('SELECT * FROM his_patients WHERE pat_id = %s', (admin_id,))
    admin = cursor.fetchone()

    if request.method == 'POST':
        # Get the updated data from the form
        fname = request.form['pat_fname']
        lname = request.form['pat_lname']
        timein = request.form['timein']
        pat_ailment = request.form['pat_ailment']
        pat_type = request.form['pat_type']

        # Update the admin data in the database
        cursor.execute('UPDATE his_patients SET pat_fname= %s,pat_lname= %s,timein= %s,pat_ailment= %s,pat_type= %s WHERE pat_id = %s',
                       (fname, lname, timein, pat_ailment, pat_type, admin_id))
        mysql.connection.commit()

        flash('Admin updated successfully!', 'success')
        return redirect('/instudentpage')

    return render_template('updatesinglestudent.html',admin=admin)



@app.route('/updatesinglestudent1/<int:admin_id>', methods=['GET', 'POST'])
def edit_admin1(admin_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)


    # Fetch the admin data by ID
    cursor.execute('SELECT * FROM his_patients WHERE pat_id = %s', (admin_id,))
    admin = cursor.fetchone()

    if request.method == 'POST':
        # Get the updated data from the form
        fname = request.form['pat_fname']
        lname = request.form['pat_lname']
        timeout = request.form['timeout']
        pat_ailment = request.form['pat_ailment']
        pat_type = request.form['pat_type']

        # Update the admin data in the database
        cursor.execute('UPDATE his_patients SET pat_fname= %s,pat_lname= %s,timeout= %s,pat_ailment= %s,pat_type= %s WHERE pat_id = %s',
                       (fname, lname, timeout, pat_ailment, pat_type, admin_id))
        mysql.connection.commit()

        flash('Admin updated successfully!', 'success')
        return redirect('/managestudent')

    return render_template('updatestudent.html',admin=admin)







@app.route('/index')  
def index():
    render_template('index.html')  

@app.route('/his_admin_view_single_student')  
def his_admin_view_single_student():
    render_template('his_admin_view_single_student.html')    
                


@app.route('/dashboard')  
def dashboard():
    cursor=mysql.connection.cursor() 
    cursor.execute("SELECT * FROM his_patients")
    data =cursor.fetchall()

    total_students_query = "SELECT COUNT(*) FROM his_patients WHERE pat_type = 'Outstudent'"
    cursor.execute(total_students_query)
    total_students = cursor.fetchone()[0]

    total_students_query = "SELECT COUNT(*) FROM his_patients WHERE pat_type = 'Instudent'"
    cursor.execute(total_students_query)
    Instudent = cursor.fetchone()[0]



    return render_template('dashboard.html', his_patients=data,total_students=total_students ,Instudent=Instudent)


@app.route('/outstudent')
def outstudent():
    connection = create_connection()
    if connection:
        try:
            # Get the count of students with pat_type = 'Instudent'
            with connection.cursor() as cursor:
                result = "SELECT count(*) FROM his_patients WHERE pat_type = 'Instudent'"
                cursor.execute(result)
                outstudent_count = cursor.fetchone()[0]
        except Error as e:
            print("Error: ", e)
            outstudent_count = None
        finally:
            connection.close()
    else:
    
        outstudent_count = None
    return render_template('dashboard.html', his_patients=data)  
    


@app.route('/Instudent')
def Instudent():
    connection = create_connection()
    if connection:
        try:
            # Get the count of students with pat_type = 'Instudent'
            with connection.cursor() as cursor:
                result = "SELECT count(*) FROM his_patients WHERE pat_type = 'Instudent'"
                cursor.execute(result)
                instudent_count = cursor.fetchone()[0]
        except Error as e:
            print("Error: ", e)
            instudent_count = None
        finally:
            connection.close()
    else:
    
        instudent_count = None
    return render_template('dashboard.html', his_patients=data)   
         

@app.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    students=studentModel.query.filter_by(id=id).first()
    if request.method== 'POST':
        if students:
            db.session.delete(students)
            de.session.commit()
            return redirect('/dashboard')
        return render_template('delete.html')  




# @app.route('/<int:pat_id>/edit', methods=['GET','POST'])
# def edit(pat_id):
#     conn = mysql.connect()
#     cursor = conn.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute('SELECT * FROM his_patients WHERE pat_id = %s', (pat_id))
#     data =cursor.fetchall()
# #     print(data[0])
#     return render_template(viewsinglestudent.html,his_patients=data[0])

@app.route('/view1/<pat_id>', methods=['GET','POST'])
def edit(pat_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM his_patients WHERE pat_id = %s', (pat_id))
    data =cursor.fetchall()
    return render_template('viewsinglestudent.html',his_patients=data[0])  

@app.route('/view2/<pat_id>', methods=['GET','POST'])
def edit2(pat_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM his_patients WHERE pat_id = %s', (pat_id))
    data =cursor.fetchall()
    return render_template('viewsinglestudent.html',his_patients=data[0])  

@app.route('/view3/<pat_id>', methods=['GET','POST'])
def edit3(pat_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM his_patients WHERE pat_id = %s', (pat_id))
    data =cursor.fetchall()
    return render_template('viewsinglestudent.html',his_patients=data[0])        

@app.route('/view4/<pat_id>', methods=['GET','POST'])
def edit4(pat_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM his_patients WHERE pat_id = %s', (pat_id))
    data =cursor.fetchall()
    return render_template('viewsinglestudent.html',his_patients=data[0])        

@app.route('/view5/<pat_id>', methods=['GET','POST'])
def edit5(pat_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM his_patients WHERE pat_id = %s', (pat_id))
    data =cursor.fetchall()
    return render_template('viewsinglestudent.html',his_patients=data[0])            




@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'pat_fname' in request.form and 'pat_lname' in request.form and 'email' in request.form and 'pat_addr' in request.form and 'pat_phone' in request.form and 'password' in request.form:
        userName = request.form['pat_fname']
        userfName = request.form['pat_lname']
        email = request.form['email']
        userprogram = request.form['pat_addr']
        userphone = request.form['pat_phone']
        password = request.form['password']

    
        length = 5
        pat_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM his_patients WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not userName or not password or not email:
            message = 'Please fill out the form!'
        else:
            # Insert the random character into the user details
            cursor.execute('INSERT INTO his_patients( pat_fname,pat_lname,email,pat_addr,pat_phone,pat_number,password) VALUES ( %s, %s, %s, %s, %s, %s, %s)', (userName, userfName, email, userprogram, userphone, pat_number, password))
            mysql.connection.commit()
            message = 'You have successfully registered!'
    elif request.method == 'POST':
        message = 'Please fill out the form!'
    return render_template('register.html', message=message)

    
if __name__ == "__main__":
    app.run()