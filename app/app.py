from flask import Flask, render_template, request, redirect,  url_for, flash
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
    
    if 'signup' in request.form and request.form['signup'] == 'Signup':
        print("signup clicked")
        return redirect(url_for("farmer_signup"))

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

@app.route('/farmer_signup', methods=['POST','GET'])
def farmer_signup():
    global db

    address_id = None

    if request.method == "POST":
        # Handle address details
        country = request.form["country"]
        city = request.form["city"]
        street_name = request.form["street_name"]

        # Insert address into database
        address_id = db.insert_address(country, city, street_name)
        
        # Handle user details
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        DoB = request.form["DoB"]
        DoJ = request.form["DoJ"]
        phone_number = request.form["phone_number"]
        user_name = request.form["user_name"]
        password1 = request.form["password"]
        password2 = request.form["Confirmpassword"]

        if password1 != password2:
            flash("Passwords do not match.")
            return redirect(request.url)
        
        # Insert farmer into database
        db.insert_farmer(first_name, last_name, DoB, DoJ, phone_number, address_id)
        db.farmer_sign_up(user_name,password1, first_name, last_name, DoB, DoJ, phone_number, address_id)


        return redirect(url_for("login", role="farmer"))


    return render_template('signup_farmer.html', countries=db.get_country_city_dict(), address_id = address_id)

@app.route('/farmer',methods=['POST', "GET"])
def farmer():
    try:
        farmer_data = db.get_details()
        name = farmer_data['first_name'] + " " + farmer_data['last_name']
        phonenumber = farmer_data['phone_number']
        farmerid = farmer_data['farmer_id']

        if request.method == "POST":
            if request.form['action'] == 'plot':
                return redirect(url_for('plot'))
            elif request.form['action'] == 'depot':
                return redirect(url_for('depot'))
            elif request.form['action'] == 'product':
                return redirect(url_for('product'))
            elif request.form['action'] == 'query':
                return redirect(url_for('query',query = request.form['query']))

        return render_template('farmer.html', username = db.user_name, name = name, phone_number = phonenumber,farmer_id = farmerid)
        
    except:
        return "Not logged in"     

@app.route('/farmer/query',methods=['GET'])
def query():
    query = request.args.get('query')
    result = db.dql_to_dictList(query)
    if result == None:
        return "Invalid Query"
    return render_template('query.html', query = query, result = result)

@app.route('/farmer/plot', methods=['GET', 'POST'])
def plot():
    
    if request.method == "POST":
        db.insert_plot(request.form['plot_size'], request.form['longitude'], request.form['latitude'])

    return render_template('')


@app.route('/farmer/depot', methods=['GET', 'POST'])
def depot():

    if request.method == "POST":
        db.insert_depot(request.form['depot_id'])

    return render_template('')


@app.route('/farmer/product', methods=['GET', 'POST'])
def product():

    if request.method == "POST":
        db.insert_product(request.form['product_id'], request.form['quantity'], request.form['depot_id'])

    return render_template('')
    # code for farmer's product page       

if __name__ == '__main__':
    app.run()