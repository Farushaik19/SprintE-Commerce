import pymysql
hostname = 'localhost'
user = 'root'
password = 'Saibaba@123'
database = 'Ecom'

db = pymysql.connections.Connection(
    host=hostname,
    user=user,
    password=password,
    database=database
)


