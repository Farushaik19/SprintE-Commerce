import pymysql
hostname = 'localhost'
user = 'root'
password = 'root'

db = pymysql.connections.Connection(
    host=hostname,
    user=user,
    password=password
)
