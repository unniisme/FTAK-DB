from flask import Flask
from api.database import PostgresqlDB

app = Flask(__name__)

## Dbdef
#Defining Db Credentials
USER_NAME = 'postgres'
PASSWORD = 'postgres'
PORT = 5432
DATABASE_NAME = 'ftak'  #Created via psql
HOST = 'localhost'

#Initializing SqlAlchemy Postgresql Db Instance
db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)

@app.route('/')
def home():
    return 'Connected'

if __name__ == '__main__':
    app.run()