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

db.farmer_sign_up("shajipappan101", "nope", "Shaji", "SS", "20/04/2002", "20/04/2023", "91002918223", 3)


"""
--To Delete, run in postgres
DROP VIEW ShajiPappan101_farmer_info;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM shajipappan101;
DROP ROLE shajipappan101;
DELETE FROM farmer_login WHERE username = 'shajipappan101';
DELETE FROM farmer WHERE first_name='Shaji';
ALTER SEQUENCE farmer_farmer_id_seq RESTART WITH 5;
"""