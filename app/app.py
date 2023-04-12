from flask import Flask, render_template, request, redirect,  url_for
from api.database import FTAKdb

app = Flask(__name__)

## Dbdef
#Defining Db Credentials
USER_NAME = 'postgres'
PASSWORD = 'postgres'
PORT = 5432
HOST = 'localhost'

#Initializing SqlAlchemy Postgresql Db Instance
db = FTAKdb(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT)

@app.route('/', methods=['POST','GET'])
def home():
    if request.method =='POST':
        if 'role' in request.form:
            role = request.form['role']
            if role == 'FARMER':
                return redirect(url_for('farmerlogin'))
            if role == 'INSPECTOR':
                return redirect(url_for('inspectorlogin'))
            if role == 'CUSTOMER':
                return redirect(url_for('customerlogin'))
            return role
    return render_template('home.html')


@app.route('/farmerlogin', methods=['POST','GET'])
def farmerlogin():
    global db

    if 'username' in request.form:
        username = request.form['username']
        password = request.form['password']

        db = FTAKdb.farmer_login(username, password, HOST, PORT)
        if db==None:
            print("Unknown username or password")
        else:
            return redirect(url_for('farmer'))


    return render_template('login.html',role = 'farmer')
    
    
@app.route('/inspectorlogn', methods=['POST','GET'])
def inspectorlogin():
    if 'username' in request.form:
        username = request.form['username']
        password = request.form['password']

    return render_template('login.html',role = 'inspector')
     
    
@app.route('/customerlogin', methods=['POST','GET'])
def customerlogin():
    if 'username' in request.form:
        username = request.form['username']
        password = request.form['password']

    return render_template('login.html',role = 'customer')

@app.route('/farmer')
def farmer():
    return "Logged in as " + db.user_name 
    

if __name__ == '__main__':
    app.run()