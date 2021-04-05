from flask import Flask, render_template, request, redirect, url_for, session,jsonify,make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import json



app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Manish2221997#'
app.config['MYSQL_DB'] = 'project_employees'

mysql = MySQL(app)


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html",index=True )

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM registered_users WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html',login=True)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'),login=False)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM registered_users WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO registered_users VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg,register=True)

@app.route('/project_allocation', methods =['GET', 'POST'])

def project_allocation():
    return  render_template('project_allocation.html',project_allocation=True)
################################################################################
@app.route('/your_url',methods=['GET','POST'])


def your_url():
    if request.method=='POST':

        if os.path.exists('Final_Employee.xlsx'):
            df = pd.read_excel('C:\\Users\\Manish\\Desktop\\MANISH\\PROJECT\\Flask App\\Final_Employee.xlsx')
            headings=df.columns.ravel()
            df_empid=df[headings[0]]
            df_name=df[headings[1]]
            df_contact=df[headings[2]]
            df_office=df[headings[3]]
            df_designation=df[headings[4]]
            df_skills=df[headings[5]]
            df_rating=df[headings[6]]
            df_succesrate=df[headings[7]]
            userin_skill=request.form['requirements']
            userin_location=request.form['location']

            l1=[]
            i=0
            userin_skilllist=userin_skill.split(',')
            for empid,skill,location in zip(df_empid,df_skills,df_office):
                skill_list=skill.split(',')
                ratio_skill=check_ratio(userin_skilllist,skill_list)
                ratio_location=SequenceMatcher(lambda x: x == " ",userin_location.upper(),location.upper()).ratio()
                if ratio_skill>0.65 and ratio_location>0.85:
                                i+=1
                                l1.append({"S.No":i,
                                   "EMP ID": df_empid[empid-1] ,
                                   "Name": df_name[empid-1],
                                   "Contact": df_contact[empid-1],
                                   "Location": df_office[empid-1],
                                   "Designation": df_designation[empid-1] ,
                                   "Skill" : df_skills[empid-1],
                                   "Rating":df_rating[empid-1]  ,
                                   "Success Rate": df_succesrate[empid-1]})
        return render_template('selected.html',employee_data=l1,selected=True)


    else:
        return redirect(url_for('project_allocation'))

def check_ratio(userin_skilllist,skill_list):

    i=0

    for userin_skill in userin_skilllist:

        userin_skill=re.sub(r'([++])+',"PP",userin_skill)
        userin_skill=re.sub(r'(\W)+',"",userin_skill)

        for skill in skill_list:

            skill=re.sub(r'([++])+',"PP",skill)
            skill=re.sub(r'(\W)+',"",skill)

            ration=SequenceMatcher(lambda x: x == " ",userin_skill.upper(),skill.upper()).ratio()

            if ration>0.6:
                i+=1

    percent=(i)/(len(userin_skilllist))
    return percent



@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404
