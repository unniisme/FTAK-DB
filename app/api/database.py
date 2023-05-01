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
        """
        For a query output, returns a list of dictionaries of the form [{column: value}]
        """
        results = []
        for entry in [x for x in dql_output]:
            results.append({key : val for val, key in (zip(entry, dql_output.keys()))})
        return results

    def dql_output_to_tupleList(dql_output):
        """
        For a query output, returns a list of dictionaries of the form [(columns), (row 1), (row 2)...]
        """
        return [tuple(dql_output.keys())] + [tuple(entry) for entry in dql_output]

    def dql_to_dictList(self, query):
        result = self.execute_dql_commands(query)
        return FTAKdb.dql_output_to_dictList(result)

    def dql_to_tupleList(self, query):
        result = self.execute_dql_commands(query)
        return FTAKdb.dql_output_to_tupleList(result)

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

    def get_cities_from_country_name(self, name):
        query = f"SELECT city_id, city.name \
            FROM city, country \
            WHERE city.country_id = country.country_id AND country.name = '{name}'"

        return self.dql_to_dictList(query)

    def get_country_city_dict(self):
        countries = set([entry['name'] for entry in self.get_countries()])
        print(self.get_cities_from_country_name('Canada'))

        return {country : [entry['name'] for entry in self.get_cities_from_country_name(country)] for country in countries}

    def get_address(self, address_id):
        query = f"SELECT address_id, country.name, city.name, street_name, stree_number, postal_code\
            FROM address NATURAL JOIN country NATURAL JOIN city \
                WHERE address_id = {address_id}"

        return self.dql_output_to_dictList(query)[0]
    
    def get_all_depots(self):
        query = "SELECT * from depot"
        return self.dql_to_dictList(query)
    
    def get_all_products(self):
        query = "SELECT * from product"
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

        if len(self.dql_to_dictList(f"SELECT address_id FROM address WHERE city_id={city_id} AND country_id={country_id} AND street_name='{street_name}'")) == 0:
            query = f"INSERT INTO address(city_id, country_id, street_name, street_number, postal_code)\
                VALUES ({city_id}, {country_id}, '{street_name}', '{street_number}', '{postal_code}')"
            self.execute_ddl_and_dml_commands(query)
            print("Inserted address")
        else:
            print("Address already exists")
        

        address_id = self.dql_to_dictList(f"SELECT address_id FROM address WHERE city_id={city_id} AND country_id={country_id} AND street_name='{street_name}'")[0]['address_id']
        return address_id

    
    # Roles and logins
    def farmer_login(username, password, host, port):
        db = FTAKdb(admin_username, admin_password, host, port)
        if (len(db.dql_to_dictList(f"SELECT * FROM farmer_login WHERE username='{username}'")) == 0):
            #Unknown username
            print("unknown username")
            return None
        
        db = FARMERdb(username, password, host, port)
        # Farmer has access to country table
        if db.execute_dql_commands("SELECT * FROM country") == None:
            #Unknown password
            print("unknown password")
            return None

        return db

    def inspector_login(username, password, host, port):

        db = INSPECTORdb(username, password, host, port)
        # inspector has access to farmer table
        if db.execute_dql_commands("SELECT * FROM farmer") == None:
            #Unknown username or password
            return None

        return db

    def customer_login(username, password, host, port):
        db = FTAKdb(username, password, host, port)

        ## Dk what restriction rn
        # if db.execute_dql_commands("SELECT * FROM ") == None:
        #     #Unknown password
        #     return None

        return db


    def farmer_sign_up(self, username, password, first_name, last_name, DoB, DoJ, phone_number, address_id):
        if len(self.dql_to_dictList(f"SELECT * FROM farmer_login WHERE username='{username}'")) != 0:
            print("User already exists")
            return -1

        with self.engine.connect() as connection:
            trans = connection.begin()
            try:                
                role_query = f"CREATE ROLE {username} LOGIN PASSWORD '{password}'"
                connection.execute(text(role_query))
                print("Created role", username)

                new_farmer_id = self.insert_farmer(first_name, last_name, DoB, DoJ, phone_number, address_id)
                farmer_login_query = f"INSERT INTO farmer_login VALUES('{username}', {new_farmer_id})"
                connection.execute(text(farmer_login_query))
                print("Created farmer")

                # Access all information about yourself
                view_query=f"CREATE VIEW {username}_farmer_info AS \
                    SELECT f.*, fp.farmer_product_id, fp.product_id, fp.quantity, fp.depot_id, fpl.plot_id, fpl.plot_size, fpl.longitude, fpl.latitude \
                    FROM farmer f \
                    LEFT JOIN farmer_plot fpl ON fpl.farmer_id = f.farmer_id \
                    LEFT JOIN farmer_product fp ON fp.farmer_id = f.farmer_id \
                    WHERE f.farmer_id = {new_farmer_id}"
                connection.execute(text(view_query))
                print("Created view")

                # Access all information about the requests that you have made
                request_view_query=f"CREATE VIEW {username}_requests AS \
                    SELECT fpla.*, fda.*, fpra.*\
                    FROM farmer \
                    LEFT JOIN farmer_plot_approval fpla ON fpla.farmer_id = farmer.farmer_id \
                    LEFT JOIN farmer_depot_approval fda ON fda.farmer_id = farmer.farmer_id \
                    LEFT JOIN farmer_product_approval fpra ON fpra.farmer_id = farmer.farmer_id \
                    WHERE farmer.farmer_id = {new_farmer_id}"


                permissions_query=f"GRANT SELECT, INSERT, UPDATE, DELETE ON {username}_farmer_info TO {username}; \
                    GRANT Farmer TO {username}"
                connection.execute(text(permissions_query))
                print("Granted permissions")

                connection.execute(text("COMMIT;"))
                connection.execute(text("END;"))

                trans.commit()

            except Exception as e:
                trans.rollback()
                print("Rolling Back")
                print(e)

        return 0

class INSPECTORdb(FTAKdb):

    def approve_farmer_plot(self, entry_id):
        query = f"UPDATE farmer_plot_approval SET approved = TRUE WHERE id = {entry_id}"

        self.execute_ddl_and_dml_commands(query)

    def update_farmer_plot(self):
        self.execute_ddl_and_dml_commands("SELECT approve_farmer_plot_requests()")

    def approve_farmer_depot(self, entry_id):
        query = f"UPDATE farmer_depot_approval SET approved = TRUE WHERE id = {entry_id}"

        self.execute_ddl_and_dml_commands(query)

    def update_farmer_depot(self):
        self.execute_ddl_and_dml_commands("SELECT approve_farmer_depot_requests()")

    def approve_farmer_product(self, entry_id):
        query = f"UPDATE farmer_product_approval SET approved = TRUE WHERE id = {entry_id}"

        self.execute_ddl_and_dml_commands(query)

    def update_farmer_product(self):
        self.execute_ddl_and_dml_commands("SELECT approve_farmer_product_requests()")

    def approve_new_farmer_product(self, entry_id):
        query = f"UPDATE new_product_approval SET approved = TRUE WHERE id = {entry_id}"

        self.execute_ddl_and_dml_commands(query)

    def update_farmer_product(self):
        self.execute_ddl_and_dml_commands("SELECT insert_approved_products()")

    def getApprovalList(self, tableName):
        """
        table names can be plot, depot, product or new_product
        """
        if tableName not in ["plot", "depot", "product"]:
            print("Unknown table")
            return -1

        if tableName == "new_product":
            query = f"SELECT * FROM {tableName}_approval"
            return self.dql_to_dictList(query)


        query = f"SELECT * FROM farmer_{tableName}_approval"
        return self.dql_to_dictList(query)


class FARMERdb(FTAKdb):

    def __init__(self, username, password, host, port):

        super().__init__(username, password, host, port)

        self.farmer_info_view = (self.user_name) + "_farmer_info"

    # DQ
    def get_details(self):
        return self.dql_to_dictList(f"SELECT farmer_id, first_name, last_name, dob, doj, phone_number, address_id FROM {self.farmer_info_view};")[0]

    def get_depots(self):
        query = f"SELECT i.depot_id, depot.name, depot.address_id  FROM {self.farmer_info_view} as i LEFT JOIN depot ON i.depot_id = depot.depot_id"

        print(query)
        return self.dql_to_dictList(query)

    def get_plots(self):
        query = f"SELECT plot_id, plot_size, longitude, latitude FROM {self.farmer_info_view}"
        return self.dql_to_dictList(query)

    def get_products(self):
        query = f"SELECT p.product_id, p.name, p.description, p.rate, p.image_link FROM {self.farmer_info_view} as i LEFT JOIN product as p ON i.product_id = p.product_id"
        return self.dql_to_dictList(query)
        

    # DD DM
    def insert_plot_request(self, plot_size, longitude, latitude):
        query = f"INSERT INTO farmer_plot_approval (farmer_id, plot_size, longitude, latitude, approved, entry_time) \
            VALUES ({self.get_details()['farmer_id']}, {plot_size}, {longitude}, {latitude}, FALSE, NOW());"
        self.execute_ddl_and_dml_commands(query)

    def insert_depot_request(self, depot_id):
        query = f"INSERT INTO farmer_depot_approval (farmer_id, depot_id, approved, entry_time) \
                VALUES ({self.get_details()['farmer_id']}, {depot_id}, FALSE, NOW());"
        self.execute_ddl_and_dml_commands(query)

    def insert_product_request(self, product_id, quantity, depot_id):
        query = f"INSERT INTO farmer_product_approval (farmer_id, product_id, quantity, depot_id, approved, entry_time) \
                VALUES ({self.get_details()['farmer_id']}, {product_id}, {quantity}, {depot_id}, FALSE, NOW());"
        self.execute_ddl_and_dml_commands(query)

    def insert_new_product_request(self, product_name, description, rate, image_link, quantity, depot_id):
        query = f"INSERT INTO new_product_approval (farmer_id, name, description, rate, image_link, approved, entry_time) \
                VALUES ({self.get_details()['farmer_id']}, {product_name}, {description}, {rate}, {image_link}, FALSE, NOW());"
        self.execute_ddl_and_dml_commands(query)
