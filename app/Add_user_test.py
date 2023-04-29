from api.database import FTAKdb

#Defining Db Credentials
USER_NAME = 'postgres'
PASSWORD = 'postgres'
PORT = 5432
HOST = 'localhost'

#Initializing SqlAlchemy Postgresql Db Instance
db = FTAKdb(user_name=USER_NAME,
                password=PASSWORD,
                host=HOST,port=PORT)

db.farmer_sign_up("cassie", "pass", "Cassie", "Smith", "20/04/2001", "21/04/2023", "9189462123", 2)


"""
--To Delete, run in postgres
DROP VIEW cassie_farmer_info;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM cassie;
DROP ROLE cassie;
DELETE FROM farmer_login WHERE username = 'cassie';
DELETE FROM farmer WHERE first_name='cassie';
ALTER SEQUENCE farmer_farmer_id_seq RESTART WITH 5;
"""