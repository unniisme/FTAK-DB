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

db.farmer_sign_up("abuarakkal", "atombomb", "Arakkal", "Abu", "21/04/2004", "20/04/2023", "91002918223", 3)


"""
--To Delete, run in postgres
DROP VIEW abuarakkal_farmer_info;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM abuarakkal;
DROP ROLE abuarakkal;
DELETE FROM farmer_login WHERE username = 'abuarakkal';
DELETE FROM farmer WHERE first_name='Arakkal';
ALTER SEQUENCE farmer_farmer_id_seq RESTART WITH 5;
"""