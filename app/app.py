from flask import Flask, render_template, request, redirect,  url_for, flash
from api.database import FTAKdb

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['FLASH_MESSAGE_DURATION'] = 10

## Dbdef
#Defining Db Credentials
USER_NAME = 'postgres'
PASSWORD = 'postgres'
PORT = 5432
HOST = 'localhost'

# Dbs login for each user
dbs = {}

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
        return redirect(url_for(client+"_signup"))

    if 'username' in request.form:
        username = request.form['username']
        password = request.form['password']

        if client == "farmer":
            dbs[request.remote_addr] = FTAKdb.farmer_login(username, password, HOST, PORT)
        elif client == "inspector":
            dbs[request.remote_addr] = FTAKdb.inspector_login(username, password, HOST, PORT)
        elif client == "customer":
            dbs[request.remote_addr] = FTAKdb.customer_login(username, password, HOST, PORT)
            
        if dbs[request.remote_addr]==None:
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
        db.farmer_sign_up(user_name, password1, first_name, last_name, DoB, DoJ, phone_number, address_id)


        return redirect(url_for("login", role="farmer"))


    return render_template('signup_farmer.html', countries=db.get_country_city_dict(), address_id = address_id)


@app.route('/customer_signup', methods=['POST','GET'])
def customer_signup():
    global db

    if request.method == "POST":
        
        # Handle user details
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        user_name = request.form["user_name"]
        password1 = request.form["password"]
        password2 = request.form["Confirmpassword"]

        if password1 != password2:
            flash("Passwords do not match.")
            return redirect(request.url)
        
        # Insert customer into database
        db.customer_sign_up(user_name, password1, first_name, last_name, email, phone_number)


        return redirect(url_for("login", role="customer"))


    return render_template('signup_customer.html')

@app.route('/customer', methods=['POST', 'GET'])
def customer():

    if request.method == "POST":
        # if request.form['action'] == 'viewRequests':
            # Insert the code to return view; View given by {username}_requests
        # else:
            dbs[request.remote_addr].insert_trade_request(request.form["product"], request.form["quantity"])

    return render_template('customer.html', products = dbs[request.remote_addr].get_products())


@app.route('/farmer',methods=['POST', "GET"])
def farmer():
    try:
        farmer_data = dbs[request.remote_addr].get_details()
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

        return render_template('farmer.html', username = dbs[request.remote_addr].user_name, name = name, phone_number = phonenumber,farmer_id = farmerid)
        
    except:
        return "Not logged in"     

@app.route('/farmer/query',methods=['GET'])
def query():
    query = request.args.get('query')

    try:
        result = dbs[request.remote_addr].dql_to_dictList(query)
        return render_template('query.html', query = query, result = result)
    except Exception as e:
        return str(e)
    
@app.route('/farmer/plot', methods=['GET', 'POST'])
def plot():
    
    if request.method == "POST":
        dbs[request.remote_addr].insert_plot_request(request.form['plot_size'], request.form['longitude'], request.form['latitude'])

    return render_template('plot.html', result = dbs[request.remote_addr].get_plots())


@app.route('/farmer/depot', methods=['GET', 'POST'])
def depot():

    if request.method == "POST":
        
        dbs[request.remote_addr].insert_depot_request(request.form['depot'])

    depots = dbs[request.remote_addr].get_all_depots()
    return render_template('depot.html',result = dbs[request.remote_addr].get_depots(),depots = depots)


@app.route('/farmer/product', methods=['GET', 'POST'])
def product():

    if request.method == "POST":
        if request.form['product'] == 'newProduct':
            product_id = request.form['product_name']
            description =  request.form['description']
            dbs[request.remote_addr].insert_new_product_request(product_id,description, request.form['rate'], request.form['image_link'],request.form['quantity'], request.form['depot_id'])
        else:
            product_id = request.form['product']
            quantity = request.form['quantity']
            depot = request.form['depot_id']
            print("product id="+str(product_id))
            print("depot_id="+str(depot))
            dbs[request.remote_addr].insert_product_request(product_id, quantity, depot)
                
    products = dbs[request.remote_addr].get_all_products()
    depots = dbs[request.remote_addr].get_all_depots()
    return render_template('product.html',result = dbs[request.remote_addr].get_products(),products = products, depots = depots)
    # code for farmer's product page     


@app.route('/inspector',methods=['POST', "GET"])
def inspector():
    try:
        if request.method == "POST":
            if request.form['action'] == 'plot':
                return redirect(url_for('approveplot'))
            elif request.form['action'] == 'depot':
                return redirect(url_for('approvedepot'))
            elif request.form['action'] == 'product':
                return redirect(url_for('approveproduct'))
            elif request.form['action'] == 'trade':
                return redirect(url_for('approvetrade'))
            elif request.form['action'] == 'query':
                return redirect(url_for('query',query = request.form['query']))

        return render_template('inspector.html', username = dbs[request.remote_addr].user_name)
        
    except:
        return "Not logged in"     
    
    
@app.route('/inspector/approveplot', methods=['GET', 'POST'])
def approveplot():
    if request.method == 'POST':
        plot_ids = request.form.getlist('plot_ids')
        if plot_ids:
        # plot_ids is a list of plot IDs that were checked
            for plot_id in plot_ids:
                dbs[request.remote_addr].approve_farmer_plot(plot_id)
            flash('Selected plots have been approved!', 'success')
        else:
            flash('Please select at least one plot to approve.', 'warning')
   
    return render_template('approve_plot.html', result=dbs[request.remote_addr].getApprovalDict('plot'))


@app.route('/inspector/approvedepot', methods=['GET', 'POST'])
def approvedepot():
    if request.method == 'POST':
        depot_ids = request.form.getlist('depot_ids')
        if depot_ids:
            for depot_id in depot_ids:
                dbs[request.remote_addr].approve_farmer_depot(depot_id)
            flash('Selected depots have been approved!', 'success')
        else:
            flash('Please select at least one depot to approve.', 'warning')
    result = dbs[request.remote_addr].getApprovalDict('depot')
    return render_template('approve_depot.html', result=result)


@app.route('/inspector/approveproduct', methods=['GET', 'POST'])
def approveproduct():

    if request.method == 'POST':
        product_ids = request.form.getlist('product_ids')
        if product_ids:
            for product_id in product_ids:
                dbs[request.remote_addr].approve_farmer_product(product_id)
            flash('Selected products have been approved!', 'success')
        else:
            flash('Please select at least one product to approve.', 'warning')
    
    return render_template('approve_product.html', result = dbs[request.remote_addr].getApprovalDict('product'))

@app.route('/inspector/approvetrade', methods=['GET', 'POST'])
def approvetrade():
    if request.method == 'POST':
        request_ids = request.form.getlist('request_ids')
        if request_ids:
           
                for request_id in request_ids:
                    try:
                        dbs[request.remote_addr].approve_trade_request(request_id)
                        dbs[request.remote_addr].update_trade()
                        flash('Selected trades have been approved!', 'success')
                    except Exception as e:
                        flash(e,'failure')
        else:
            flash('Please select at least one trade to approve.', 'warning')
    result = dbs[request.remote_addr].get_trade_requests()
    return render_template('approve_trade.html', trade=dbs[request.remote_addr].get_trade_readable(), result=result)



if __name__ == '__main__':
    app.run()