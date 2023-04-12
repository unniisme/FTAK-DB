from flask import Flask, render_template, request
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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<farmer_id>')
def getFarmer(farmer_id):
    return str(db.get_farmer_by_id(farmer_id))

if __name__ == '__main__':
    app.run()