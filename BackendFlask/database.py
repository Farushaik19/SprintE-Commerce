import pymysql
hostname = 'localhost'
user = 'root'
password = 'root'
database = 'Ecom'

db = pymysql.connections.Connection(
    host=hostname,
    user=user,
    password=password,
    database=database
)


