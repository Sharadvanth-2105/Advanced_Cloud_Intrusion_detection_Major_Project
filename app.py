import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import sqlite3

import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
import pandas as pd
import numpy as np
import pickle
import sqlite3
import random

import smtplib 
from email.message import EmailMessage
from datetime import datetime

warnings.filterwarnings('ignore')



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/home1')
def home1():
	return render_template('home1.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')



@app.route("/signup")
def signup():
    global otp, username, name, email, number, password
    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    otp = random.randint(1000,5000)
    print(otp)
    msg = EmailMessage()
    msg.set_content("Your OTP is : "+str(otp))
    msg['Subject'] = 'OTP'
    msg['From'] = "vandhanatruprojects@gmail.com"
    msg['To'] = email
    
    
    # s = smtplib.SMTP('smtp.gmail.com', 587)
    # s.starttls()
    # s.login("vandhanatruprojects@gmail.com", "pahksvxachlnoopc")
    # s.send_message(msg)
    # s.quit()
    # return render_template("val.html")

    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signin.html")

'''
@app.route('/predict1', methods=['POST'])
def predict1():
    global otp, username, name, email, number, password
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        if int(message) == otp:
            print("TRUE")
            con = sqlite3.connect('signup.db')
            cur = con.cursor()
            cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
            con.commit()
            con.close()
            return render_template("signin.html")
    return render_template("signup.html")
'''	
	

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("home.html")
    else:
        return render_template("signin.html")

@app.route("/notebook1")
def notebook1():
    return render_template("Notebook.html")

@app.route("/notebook2")
def notebook2():
    return render_template("UNSW_NB15.html")

@app.route('/predict',methods=['POST'])
def predict():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('model_kdd.sav')
    predict = model.predict(final4)

    if predict==0:
        output='There is No Attack Detected and Its Normal!'
    elif predict==1:
        output='Attack is Detected and its Probe Attack!'
    elif predict==2:
        output='Attack is Detected and its R2L Attack!'
    elif predict==3:
        output='Attack is Detected and its U2R Attack!'
    elif predict==4:
        output='Attack is Detected and its DOS Attack!'
    
    

    return render_template('prediction.html', output=output)

@app.route('/predict2',methods=['POST'])
def predict2():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('model_unsw.sav')
    predict = model.predict(final4)

    if predict==1:
        output='There is No Attack Detected and Its Normal!'
    elif predict==0:
        output='Attack is Detected!'
   
    
    

    return render_template('prediction1.html', output=output)


if __name__ == "__main__":
    app.run(debug=True)
