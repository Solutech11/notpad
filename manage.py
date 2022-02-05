from tabnanny import check
from flask import Flask, flash,redirect,url_for,render_template,request,session
from mydb import mycursor, mydb
import time


app=Flask(__name__)
app.secret_key= "naira-dollar"
def timer():
    return time.ctime()

@app.route('/')
def home():
    if 'accountnote' in session:
        # assigning session to variable: it makes code easier because u wont need to create route just ur session nd u are good to go
        user= session['accountnote']


        # searching for the account
        mycursor.execute(f'SELECT * FROM user WHERE email="{user}"')
        userdetails= mycursor.fetchone()

        # search for all user notes 
        mycursor.execute(f'SELECT * FROM notes WHERE email="{user}"')
        usersNote= mycursor.fetchall()

        return render_template('index.html', user=userdetails, notes=usersNote)
    else:
        return redirect('/login')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'accountnote' in session:
        if request.method=='POST':
            _title=request.form['title']
            _note=f'''{request.form["note"]}'''
            time = timer()
            email= session['accountnote']
            mycursor.execute(f'INSERT INTO notes(email, Date, Title,notes) VALUES("{email}","{time}","{_title}","{_note}")')
            mydb.commit()
            flash('Success')
            return redirect('/')
        if request.method=='GET':
            return render_template('add.html')
    else:
        flash('Not logged in yet')
        return redirect('/')
    # return 'adding page, ok warrisi'



@app.route('/delete/<int:id>')
def delete(id):
    if 'accountnote' in session:
        account= session['accountnote']

        mycursor.execute(f'SELECT * FROM notes WHERE email="{account}" AND id="{id}"')
        check= mycursor.fetchone()
        if check:
            mycursor.execute(f'DELETE FROM notes WHERE email="{account}" AND id="{id}" ')
            mydb.commit
        else :
            return redirect("/")
    return redirect('/')
@app.route('/retrieve/<int:id>', methods=['GET','POST'])
def retrieve(id):
    # saving session to verify the account is already in a session +
    if 'accountnote' in session:
        accounts = f'{session["accountnote"]}'
        
        # this will check your account and the id if the both are in the table
        mycursor.execute(f'SELECT * FROM notes WHERE email="{accounts}" AND id="{id}"')
        # this will collect the note nd check if there is any note related to it 
        collectNote= mycursor.fetchone()

        if collectNote:
            if request.method=='POST':
                _title =request.form['title']
                _body = request.form['body']
                time =timer()
                mycursor.execute(f'UPDATE notes SET Title="{_title}", notes="{_body}",Date="{time}" WHERE email="{accounts}" AND id="{id}"')
                mydb.commit()
                
                return redirect(f'/retrieve/{id}')
            if request.method=='GET':
                return render_template('retrieve.html', item= collectNote)
                
        else:
            return redirect('/notfound')
    else:
        return redirect('/')

    # return f'{id}'


@app.route('/login', methods=['GET','POST'])
def login():
    txt=''
    if request.method=='POST':
        _email= request.form['email']
        _password = request.form['password']

        # to verify the login is true 
        if _email and _password:
            mycursor.execute(f'SELECT * FROM user WHERE email="{_email}" AND passworrd="{_password}"')
            verified = mycursor.fetchone()

            # if its true it will add to session
            if verified:
                session['accountnote']=f'{_email}'
                return redirect('/')
            else:
                txt='account not valid'
            
    return render_template('login.html', validator=txt)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=''
    if request.method=='POST':
        _name= request.form['name']
        _email= request.form['email']
        _password= request.form['password']

            # check if account exsist
        mycursor.execute(f'SELECT * FROM user WHERE email="{_email}"')
        available=mycursor.fetchone()
        
        if available:
            msg='Account already Available (Email already in use)'
        else:
            # Inserting account to database 
            mycursor.execute(f'INSERT INTO user(name, email, passworrd) VALUE("{_name}","{_email}", "{_password}") ')
            mydb.commit()
            # adding it to my session
            session['accountnote']=f'{_email}'
            return redirect('/')
    return render_template('register.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('accountnote', default=None)
    return redirect('/')


@app.errorhandler(404)
def bar(error):
        return render_template('404.html'), 404

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=8000,debug=True)