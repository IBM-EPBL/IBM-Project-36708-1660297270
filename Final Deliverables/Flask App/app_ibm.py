import email
from email import message
from importlib.resources import contents 
from tkinter import S
from turtle import title 
from flask import Flask, redirect,render_template, request,session, url_for, Flask
from pyexpat import model
from werkzeug.utils import secure_filename
import ibm_db
from flask_mail import Mail, Message
from markupsafe import escape
from flask import Flask,render_template,request
import requests
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "A3SrnPK-7Z8jLS9Zlcmmm-B7lFWjGtRjuPmhXXjpCvQM"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
 
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}



app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\Xec]/'

mail = Mail(app)


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=trm74992;PWD=7EVyzBSougGI2vwn",'','')
print(conn)
print("connection successful...")
@app.route('/', methods = ['GET','POST'])
def signup():
    return render_template('signup.html')




@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')



@app.route('/logout')
def logout():
    return render_template('login.html')



@app.route('/about')
def about():
    return render_template('about.html')


    
@app.route('/index')
def index():
    return render_template('index.html')


 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['uname']
        mail = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        sql = "SELECT * FROM customer WHERE email=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,mail)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

    if account:
        return render_template('index.html', msg="You are already a member, please login using your details....")
      
    else:
      insert_sql = "INSERT INTO customer VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, uname)
      ibm_db.bind_param(prep_stmt, 2, mail)
      ibm_db.bind_param(prep_stmt, 3, phone)
      ibm_db.bind_param(prep_stmt, 4, password)
      ibm_db.execute(prep_stmt)
    
    return render_template('login.html', msg="Student Data saved successfuly..")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    sec = ''
    if request.method == 'POST':
        
        mail = request.form['email']
        password = request.form['password']

        sql = f"select * from customer where email='{escape(mail)}' and password= '{escape(password)}'"
        stmt = ibm_db.exec_immediate(conn, sql)
        data = ibm_db.fetch_both(stmt)
                       
        if data:
            
            session["mail"] = escape(mail)
            session["password"] = escape(password)
            return redirect(url_for('index'))

        else:
            return render_template('login.html',msg = "Invalid email/ Password or Not registered!!?")
    
    return "not going to happen dickhead!!??"


@app.route('/prediction',methods=["POST"])
def predict():
    if request.method=="POST":
        name=request.form["name"]
        month=request.form["month"]
        if(int(month)>12):
            ans="Please Enter the correct Month"
            return render_template("index.html" ,y=ans)

        dayofmonth=request.form["dayofmonth"]
        if(int(dayofmonth)>31):
            ans="Please Enter the correct Day of Month"
            return render_template("index.html" ,y=ans)

        dayofweek=request.form["dayofweek"]
        if(int(dayofweek)>7):
            ans="Please Enter the correct Day of Week"
            return render_template("index.html" ,y=ans)
       
        
        origin=request.form["origin"]
        destination=request.form['destination']
        
        if(origin==destination):
            ans="Origin airport and destination airport can't be same"
            return render_template("index.html" ,y=ans)
        
        if(origin=="msp"):
            origin1,origin2,origin3,origin4,origin5=0,0,0,1,0
        if(origin=="dtw"):
            origin1,origin2,origin3,origin4,origin5=0,1,0,0,0
        if(origin=="jfk"):
            origin1,origin2,origin3,origin4,origin5=0,0,1,0,0
        if(origin=="sea"):
            origin1,origin2,origin3,origin4,origin5=0,0,0,0,1
        if(origin=="alt"):
            origin1,origin2,origin3,origin4,origin5=1,0,0,0,0
    
        
        
        if(destination=="msp"):
            destination1,destination2,destination3,destination4,destination5=0,0,0,1,0
        if(destination=="dtw"):
            destination1,destination2,destination3,destination4,destination5=0,1,0,0,0
        if(destination=="jfk"):
            destination1,destination2,destination3,destination4,destination5=0,0,1,0,0
        if(destination=="sea"):
            destination1,destination2,destination3,destination4,destination5=0,0,0,0,1
        if(destination=="alt"):
            destination1,destination2,destination3,destination4,destination5=1,0,0,0,0

        depthr=request.form['depthr']
        deptmin=request.form['deptmin']
        if(int(depthr)>23 or int(deptmin)>59):
            ans="Please enter the correct Departure time"
            return render_template("index.html" ,y=ans)
        else:
            dept=depthr+deptmin
       
        actdepthr=request.form['actdepthr']
        actdeptmin=request.form['actdeptmin']
        if(int(actdepthr)>23 or int(actdeptmin)>59):
            ans="Please enter the correct Actual Departure time"
            return render_template("index.html" ,y=ans)
        else:
            actdept=actdepthr+actdeptmin

       

        arrtimehr=request.form['arrtimehr']
        arrtimemin=request.form['arrtimemin']
        if(int(arrtimehr)>23 or int(arrtimemin)>59):
            ans="Please enter the correct Arrival time"
            return render_template("index.html" ,y=ans)
        else:
            arrtime=arrtimehr+arrtimemin
        
       
        if((int(actdept)-int(dept))<15):
            dept15=0
        else:
            dept15=1    

        print(dept15)
        
        total=[[int(month),int(dayofmonth),int(dayofweek),int(origin1),int(origin2),int(origin3),int(origin4),int(origin5),int(destination1),int(destination2),int(destination3),int(destination4),int(destination5),int(dept),int(actdept),int(dept15),int(arrtime)]]
        print(total)
        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": ["int(month)","int(dayofmonth)","int(dayofweek)","int(origin1)","int(origin2)","int(origin3)","int(origin4)","int(origin5)","int(destination1)","int(destination2)","int(destination3)","int(destination4)","int(destination5)","int(dept)","int(actdept)","int(dept15)","int(arrtime)"], "values": total}]}
        
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/5b2670ac-b4ed-4173-a575-bf3383144c03/predictions?version=2022-11-15', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        
        pred = response_scoring.json()
        value = pred['predictions'][0]['values'][0][0]
        
        print(value)
        if value==0:
            ans="THE FLIGHT WILL BE ON TIME"
        else:
            ans="THE FLIGHT WILL BE DELAYED"     

    return render_template("results.html" ,y=ans)    



if __name__ == "__main__":
    app.run(debug=True)