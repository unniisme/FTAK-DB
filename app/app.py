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
            return redirect(url_for('login',role = role))
            
    return render_template('home.html')


@app.route('/login', methods=['POST','GET'])
def login():
    global db

    client = request.args.get('role')
    print(client)
    if 'username' in request.form:
        username = request.form['username']
        password = request.form['password']

        if client == "farmer":
            db = FTAKdb.farmer_login(username, password, HOST, PORT)
        else:
            db = FTAKdb(username, password, host, port)
            
        if db==None:
            print("Unknown username or password")
        else:
            return redirect(url_for(client))

    return render_template('login.html',role = client)

@app.route('/farmer')
def farmer():
    return "Logged in as " + db.user_name 
    

if __name__ == '__main__':
    app.run()