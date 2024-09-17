import mysql.connector

conn = mysql.connetor.connect(host='127.0.0.1', user='root', password='password')

cursor = conn.cursor()

cursor.execute(
    'CREATE DATABASE test_mysql_database'
)

conn.close()