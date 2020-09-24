from app import app
from flaskext.mysql import MySQL 

mysql = MySQL()

# MySQL Configurations 
app.config['MySQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MySQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'braintumor'
mysql.init_app(app)

