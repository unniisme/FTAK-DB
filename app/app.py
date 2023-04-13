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
            role = request.form['role'] #farmer, inspector, customer
            return redirect(url_for('login',role = role))
            
    return render_template('home.html')


@app.route('/login', methods=['POST','GET'])
def login():
    global db

    client = request.args.get('role')
    if 'username' in request.form:
        username = request.form['username']
        password = request.form['password']

        if client == "farmer":
            db = FTAKdb.farmer_login(username, password, HOST, PORT)
        elif client == "inspector":
            db = FTAKdb.inspector_login(username, password, HOST, PORT)
        elif client == "customer":
            db = FTAKdb.customer_login(username, password, HOST, PORT)
            
        if db==None:
            print("Unknown username or password")
        else:
            return redirect(url_for(client))

    return render_template('login.html',role = client)

@app.route('/farmer_signup', methods=['POST'])
def register():
    global db

    address_id = None

    if request.method == "POST":
        # Method to define address
        if "street_name" in request.form:
            country = request.form["country"]
            city = request.form["city"]
            street_name = request.form["street_name"]

            address_id = db.insert_address(country, city, street_name)
        
        elif "first_name" in request.form:
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            DoB = request.form["DoB"]
            DoJ = request.form["first_name"]
            phone_number = request.form["phone_number"]
            address_id = request.form["address_id"]

            db.insert_farmer(first_name, last_name, DoB, DoJ, phone_number, address_id)

            return redirect(url_for("login", role="farmer"))


    return render_template('signup.html', countries=db.get_country_city_dict(), address_id = address_id)

@app.route('/farmer')
def farmer():
    return "Logged in as " + db.user_name 

if __name__ == '__main__':
    app.run()