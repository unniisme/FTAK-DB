import sqlalchemy
from sqlalchemy.engine import create_engine
from sqlalchemy.sql import text

admin_username = "postgres"
admin_password = "postgres" #Suppose to be hidden

# Database Connection
class PostgresqlDB:
    def __init__(self,user_name,password,host,port,db_name):
        """
        class to implement DDL, DQL and DML commands,
        user_name:- username
        password:- password of the user
        host
        port:- port number
        db_name:- database name
        """
        self.user_name = user_name
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.engine = self.create_db_engine()
        self.session_dict = {}

    def create_db_engine(self):
        """
        Method to establish a connection to the database, will return an instance of Engine
        which can used to communicate with the database
        """
        try:
            db_uri = f"postgresql+psycopg2://{self.user_name}:{self.password}@{self.host}:{self.port}/{self.db_name}"
            return create_engine(db_uri)
        except Exception as err:
            raise RuntimeError(f'Failed to establish connection -- {err}') from err

    def execute_dql_commands(self,stmnt,values=None):
        """
        DQL - Data Query Language
        SQLAlchemy execute query by default as 

        BEGIN
        ....
        ROLLBACK 

        BEGIN will be added implicitly everytime but if we don't mention commit or rollback explicitly 
        then rollback will be appended at the end.
        We can execute only retrieval query with above transaction block.If we try to insert or update data 
        it will be rolled back.That's why it is necessary to use commit when we are executing 
        Data Manipulation Langiage(DML) or Data Definition Language(DDL) Query.
        """
        try:
            with self.engine.connect() as conn:
                if values is not None:
                    result = conn.execute(text(stmnt),values)
                else:
                    result = conn.execute(text(stmnt))
            return result
        except Exception as err:
            print(f'Failed to execute dql commands -- {err}')
    
    def execute_ddl_and_dml_commands(self,stmnt,values=None):
        """
        Method to execute DDL and DML commands
        here we have followed another approach without using the "with" clause
        """
        connection = self.engine.connect()
        trans = connection.begin()
        try:
            if values is not None:

                result = connection.execute(text(stmnt),values)
            else:
                result = connection.execute(text(stmnt))
            trans.commit()
            connection.close()
            print('Command executed successfully.')
        except Exception as err:
            trans.rollback()
            print(f'Failed to execute ddl and dml commands -- {err}')


class FTAKdb(PostgresqlDB):
    """
    Queries for the ftak database
    """

    #Type functions
    def dql_output_to_dictList(dql_output):
        results = []
        for entry in [x for x in dql_output]:
            results.append({key : val for val, key in (zip(entry, dql_output.keys()))})
        return results

    def dql_to_dictList(self, query):
        result = self.execute_dql_commands(query)
        return FTAKdb.dql_output_to_dictList(result)

    def print_dql(self, query):
        result = self.execute_dql_commands(query)

        [print("| {:^20} |".format(column), end="") for column in result.keys()]
        print("")
        for row in result:
            [print("| {:^20} |".format(entry), end="") for entry in row]
            print("")

        print()

    def print_table(self, table):
        self.print_dql(f"SELECT * FROM {table}") 



    def __init__(self,user_name,password,host,port):
        # Initialise parent class using database 'ftak'
        super().__init__(user_name, password, host, port, 'ftak')

    # DQ
    def get_farmer_by_id(self, id):
        query = f"SELECT * FROM farmer \
            WHERE farmer_id = {id}"
        
        return self.dql_to_dictList(query)

    def get_countries(self):
        query = "SELECT * FROM country"

        return self.dql_to_dictList(query)

    def get_citied_from_country_name(self, name):
        query = f"SELECT city_id, city.name \
            FROM city, country \
            WHERE city.country_id = country.country_id AND city.name = {name}"

        return self.dql_to_dictList(query)

    # DD DM
    def insert_farmer(self, first_name, last_name, DoB, DoJ, phone_number, address_id):
        query = f"INSERT INTO farmer(first_name, last_name, DoB, DoJ, phone_number, address_id) \
            VALUES ('{first_name}', '{last_name}', '{DoB}', '{DoJ}', {phone_number}, {address_id})"

        self.execute_ddl_and_dml_commands(query)
        print("Inserted farmer")

        # Return ID
        return self.dql_to_dictList(f"SELECT farmer_id FROM farmer WHERE first_name='{first_name}' AND last_name='{last_name}' AND phone_number='{phone_number}'")[0]['farmer_id']

    def insert_address(self, country, city=None, street_name=None, street_number=None, postal_code=None):
        if city==None or len(self.dql_to_dictList(f"SELECT * FROM country WHERE name='{country}'")) == 0:
            if len(self.dql_to_dictList(f"SELECT * FROM country WHERE name='{country}'")) > 0:
                print("Country",country, "already present")
                return -1

            query = f"INSERT INTO country(name) VALUES('{country}')"
            self.execute_ddl_and_dml_commands(query)
            print("Inserted country", country)

            if city == None:
                return 0

        country_id = self.dql_to_dictList(f"SELECT * FROM country WHERE name = '{country}'")[0]['country_id']

            
        if street_name==None or len(self.dql_to_dictList(f"SELECT * FROM city WHERE name='{city}'")) == 0:
            if len(self.dql_to_dictList(f"SELECT * FROM city WHERE name='{city}'")) > 0:
                print("City", city, "already present")
                return -1

            query = f"INSERT INTO city(name, country_id) VALUES('{city}', {country_id})"
            self.execute_ddl_and_dml_commands(query)
            print("Inserted city", city)

            if street_name == None:
                return 0

        city_id = self.dql_to_dictList(f"SELECT * FROM city WHERE name = '{city}'")[0]['city_id']

        street_number = "NULL" if street_number==None else street_number
        postal_code = "NULL" if postal_code==None else postal_code

        query = f"INSERT INTO address(city_id, country_id, street_name, street_number, postal_code)\
            VALUES ({city_id}, {country_id}, '{street_name}', '{street_number}', '{postal_code}')"
        
        self.execute_ddl_and_dml_commands(query)
        print("Inserted address")

    
    # Roles and logins
    def farmer_login(username, password, host, port):
        db = FTAKdb(admin_username, admin_password, host, port)
        if (len(db.dql_to_dictList(f"SELECT * FROM farmer_login WHERE username='{username}'")) == 0):
            #Unknown username
            return None
        
        db = FTAKdb(username, password, host, port)
        if db.execute_dql_commands("SELECT * FROM address") == None:
            #Unknown password
            return None

        return db


    def farmer_sign_up(self, username, password, first_name, last_name, DoB, DoJ, phone_number, address_id):
        if len(self.dql_to_dictList(f"SELECT * FROM farmer_login WHERE username='{username}'")) != 0:
            print("User already exists")
            return -1

        role_query = f"CREATE ROLE {username} LOGIN PASSWORD '{password}'"
        self.execute_ddl_and_dml_commands(role_query)
        print("Created role", username)

        new_farmer_id = self.insert_farmer(first_name, last_name, DoB, DoJ, phone_number, address_id)
        farmer_login_query = f"INSERT INTO farmer_login VALUES('{username}', {new_farmer_id})"
        self.execute_ddl_and_dml_commands(farmer_login_query)
        print("Created farmer")

        view_query=f"CREATE VIEW {username}_farmer_info AS \
            SELECT f.*, fp.farmer_product_id, fp.product_id, fp.quantity, fp.depot_id, fpl.plot_id, fpl.plot_size, fpl.longitude, fpl.latitude \
            FROM farmer f \
            LEFT JOIN farmer_plot fpl ON fpl.farmer_id = f.farmer_id \
            LEFT JOIN farmer_product fp ON fp.farmer_id = f.farmer_id \
            WHERE f.farmer_id = {new_farmer_id}"
        self.execute_ddl_and_dml_commands(view_query)
        print("Created view")



        permissions_query=f"GRANT SELECT, INSERT, UPDATE, DELETE ON {username}_farmer_info TO {username}; \
            GRANT SELECT ON product TO {username}; \
            GRANT SELECT ON address TO {username}; \
            GRANT SELECT ON country TO {username}; \
            GRANT SELECT ON city TO {username}; \
            GRANT SELECT ON depot TO {username}"
        self.execute_ddl_and_dml_commands(permissions_query)
        print("Granted permissions")

        return 0
