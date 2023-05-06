# FTAK-DB

A database and frontend to access and manage different farmer and customer details in a presumed database of the Fair Trade Alliances, Kerala.

---

## Database
Written in PSQL. The definition of the database can be found in `db-definitions`.  
Involves tables, roles, functions, triggers, views and indices required for the database.

## Backend
Backend is written in Python (SQLAlchemy and psycopg2). Can be found in `app/api/database.py`.  
Involves all the calls to the database required to be made from front end as well as some database functions which require more elaborate code to write, such as defining an individual table for each farmer on creation of a farmer user.

## Frontend
Written in  Python (Flask), HTML, JavaScript and CSS. Code can be found in `app/app.py`, `app/templates/` and `app/static`.  
Front end is a website that provides access to sign up and log in pages for Customers and Farmers, platform for Farmers to put up requests for adding Plots, Products and Depots to their profile, for customers to request for a trade and for Inspectors to approve each of these requests.

---

## Credits
[unniisme](https://github.com/unniisme)  
[padath314](https://github.com/padath314)  
[Sujit Mandava](https://github.com/sujitmandava)