from xmlrpc import client
from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
from emailpy import *
app=Flask(__name__)



def replace_spaces_with_pluses(sample):
    """Returns a string with each space being replaced with a plus so the email hyperlink can be formatted properly"""
    changed = list(sample)
    for i, c in enumerate(changed):
        if(c == ' ' or c =='  ' or c =='   ' ):
            changed[i] = '+'
    return ''.join(changed)

@app.route("/")
@app.route("/index")
def index():
    con=sql.connect("db_web.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from UserData")
    data=cur.fetchall()
    return render_template("index.html",datas=data)

@app.route("/add_user",methods=['POST','GET'])
def add_user():
    if request.method=='POST':
        fname=request.form['fname']
        lname=request.form['lname']
        cilents=request.form['cilents']
        domine = request.form['domine']
        notes = request.form['notes']
        if 'https://www.' in domine:
            domine = domine.replace('www.','')
            domine = domine.replace('/','')
            if 'https:' in domine:
                domine = domine.replace('https:','')
        elif 'http://www.' in domine:
            domine = domine.replace('www.','')
            domine = domine.replace('/','')
            if 'http:' in domine:
                domine = domine.replace('http:','')
        elif 'http://'  in domine:
            domine = domine.replace('http://','')
            domine = domine.replace('/','')
        elif 'https://' in domine:
            domine = domine.replace('https://','')
            domine = domine.replace('/','')
        

        contact=request.form['contact']
        coumpanyemail=request.form['email']
        datetime = request.form['datetime']
        con=sql.connect("db_web.db")
        cur=con.cursor()
        cur.execute("insert into UserData(UNAME,Lastname,CONTACT,Domine,COUMPANYEMAIL,CILENTS,TIME,REMARKS,REMARKS1,REMARKS2,REMARKS3,NOTES) values (?,?,?,?,?,?,?,?,?,?,?,?)",(fname,lname,contact,domine,coumpanyemail,cilents,datetime,'Email Notsent','Email Notsent','Email Notsent','Email Notsent',notes))
        con.commit()
        flash('User Added','success')
        return redirect(url_for("index"))
    return render_template("add_user.html")

@app.route("/edit_user/<string:uid>",methods=['POST','GET'])
def edit_user(uid):
    if request.method=='POST':
        uname=request.form['uname']
        lname=request.form['lname']
        domine = request.form['domine']
        cilents = request.form['cilents']
        notes = request.form['notes']
        if 'https://www.' in domine:
            domine = domine.replace('www.','')
            domine = domine.replace('/','')
            if 'https:' in domine:
                domine = domine.replace('https:','')
        elif 'http://www.' in domine:
            domine = domine.replace('www.','')
            domine = domine.replace('/','')
            if 'http:' in domine:
                domine = domine.replace('http:','')
        elif 'http://'  in domine:
            domine = domine.replace('http://','')
            domine = domine.replace('/','')
        elif 'https://' in domine:
            domine = domine.replace('https://','')
            domine = domine.replace('/','')

        contact=request.form['contact']
        email=request.form['email']
        email1 = request.form['email1']
        email2 = request.form['email2']
        email3 = request.form['email3']
        email4 = request.form['email4']

        
        coumpanyemail = request.form['coumpanyemail']
        con=sql.connect("db_web.db")
        cur=con.cursor()
        cur.execute("update UserData set UNAME=?,Lastname=?,CONTACT=?,Domine=?,EMAIL=?,COUMPANYEMAIL=?,CILENTS=?,REMARKS=?,REMARKS1=? , REMARKS2=? , REMARKS3=? ,NOTES=? where UID=?",(uname,lname,contact,domine,email,coumpanyemail,cilents,email1,email2,email3,email4,notes,uid))
        con.commit()
        flash('User Updated','success')
        return redirect(url_for("index"))
    con=sql.connect("db_web.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from UserData where UID=?",(uid,))
    data=cur.fetchone()
    return render_template("edit_user.html",datas=data)
    
@app.route("/delete_user/<string:uid>",methods=['GET'])
def delete_user(uid):
    con=sql.connect("db_web.db")
    cur=con.cursor()
    cur.execute("delete from UserData where UID=?",(uid,))
    con.commit()
    flash('User Deleted','warning')
    return redirect(url_for("index"))

@app.route("/search",methods=['POST','GET'])
def search():
    if request.method=='POST' or request.method=='GET':
        search=request.form['searchq']
        con=sql.connect("db_web.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute(f"select * from UserData where UNAME  like '%{search}%' or Lastname like '%{search}%' or CONTACT like '%{search}%' or Domine like '%{search}%' or EMAIL like '%{search}%' or COUMPANYEMAIL like '%{search}%' or CILENTS like '%{search}%' or TIME like '%{search}%'")
        data=cur.fetchall()
        return render_template("index.html",datas=data)
    return redirect(url_for("index"))

@app.route("/genrateemail/<string:uid>",methods=['POST','GET'])
def genrateemail(uid):
    if request.method=='POST' or request.method=='GET' :
        con=sql.connect("db_web.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from UserData where UID=?",(uid,))
        data=cur.fetchone()
        firstname = data['UNAME']
        lastname = data['Lastname']
        domine = data['Domine']

        email = run(firstname,lastname,domine)
        cur.execute("update UserData set EMAIL=? where UID=?",(email,uid))
        con.commit()
        flash('Email Generated','success')
        return redirect(url_for("index"))
    return render_template("index.html")

@app.route("/sendemail/<string:uid>",methods=['POST','GET'])
def sendemail(uid):
    if request.method=='POST' or request.method=='GET' :
        con=sql.connect("db_web.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from UserData where UID=?",(uid,))
        data=cur.fetchone()
        firstname = data['UNAME']
        lastname = data['Lastname']
        domine = data['Domine']
        email = data['EMAIL']
        sub = f'''Hi {firstname} {lastname} how are you doing'''
        with open('email1.txt', encoding="utf8") as r:
            contents = r.read()
        aml = contents.replace('{firstname}',firstname)
        aml = aml.replace('{lastname}',lastname)
        aml = aml.replace('{domine}',domine)
        aml = aml.replace('{clients}',data['CILENTS'])
        # aml = f'''Dear {firstname} {lastname},\nThis is a test email.\ni llove your website {domine} \n\nThanks, '''
        url = f"https://mail.google.com/mail/?view=cm&fs=1&to={email}&su={replace_spaces_with_pluses(sub)}&body={replace_spaces_with_pluses(aml)}"
        flash('Email Send','success')
        return redirect(url)
    return render_template("index.html")



@app.route("/sendemailf1/<string:uid>",methods=['POST','GET'])
def sendemailf1(uid):
    if request.method=='POST' or request.method=='GET' :
        con=sql.connect("db_web.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from UserData where UID=?",(uid,))
        data=cur.fetchone()
        firstname = data['UNAME']
        lastname = data['Lastname']
        domine = data['Domine']
        email = data['EMAIL']
        sub = f'''Hi {firstname} {lastname} how are you doing this is followup1'''
        with open('email1.txt', encoding="utf8") as r:
            contents = r.read()
        aml = contents.replace('{firstname}',firstname)
        aml = aml.replace('{lastname}',lastname)
        aml = aml.replace('{domine}',domine)
        aml = aml.replace('{clients}',data['CILENTS'])
        # aml = f'''Dear {firstname} {lastname},\nThis is a test email.\ni llove your website {domine} \n\nThanks, '''
        url = f"https://mail.google.com/mail/?view=cm&fs=1&to={email}&su={replace_spaces_with_pluses(sub)}&body={replace_spaces_with_pluses(aml)}"
        flash('Email Send','success')
        return redirect(url)
    return render_template("index.html")



@app.route("/sendemailf2/<string:uid>",methods=['POST','GET'])
def sendemailf2(uid):
    if request.method=='POST' or request.method=='GET' :
        con=sql.connect("db_web.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from UserData where UID=?",(uid,))
        data=cur.fetchone()
        firstname = data['UNAME']
        lastname = data['Lastname']
        domine = data['Domine']
        email = data['EMAIL']
        sub = f'''Hi {firstname} {lastname} how are you doing this is followup2'''
        with open('email1.txt', encoding="utf8") as r:
            contents = r.read()
        aml = contents.replace('{firstname}',firstname)
        aml = aml.replace('{lastname}',lastname)
        aml = aml.replace('{domine}',domine)
        aml = aml.replace('{clients}',data['CILENTS'])
        # aml = f'''Dear {firstname} {lastname},\nThis is a test email.\ni llove your website {domine} \n\nThanks, '''
        url = f"https://mail.google.com/mail/?view=cm&fs=1&to={email}&su={replace_spaces_with_pluses(sub)}&body={replace_spaces_with_pluses(aml)}"
        flash('Email Send','success')
        return redirect(url)
    return render_template("index.html")


@app.route("/sendemailf3/<string:uid>",methods=['POST','GET'])
def sendemailf3(uid):
    if request.method=='POST' or request.method=='GET' :
        con=sql.connect("db_web.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from UserData where UID=?",(uid,))
        data=cur.fetchone()
        firstname = data['UNAME']
        lastname = data['Lastname']
        domine = data['Domine']
        email = data['EMAIL']
        sub = f'''Hi {firstname} {lastname} how are you doing this is followup3'''
        with open('email1.txt', encoding="utf8") as r:
            contents = r.read()
        aml = contents.replace('{firstname}',firstname)
        aml = aml.replace('{lastname}',lastname)
        aml = aml.replace('{domine}',domine)
        aml = aml.replace('{clients}',data['CILENTS'])
        # aml = f'''Dear {firstname} {lastname},\nThis is a test email.\ni llove your website {domine} \n\nThanks, '''
        url = f"https://mail.google.com/mail/?view=cm&fs=1&to={email}&su={replace_spaces_with_pluses(sub)}&body={replace_spaces_with_pluses(aml)}"
        flash('Email Send','success')
        return redirect(url)
    return render_template("index.html")

if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)