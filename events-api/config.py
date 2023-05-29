from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'eventapp'
app.config['MYSQL_DATABASE_PASSWORD'] = 'CyberArk1@3'
app.config['MYSQL_DATABASE_DB'] = 'events'
app.config['MYSQL_DATABASE_HOST'] = '10.0.99.28'
mysql.init_app(app)