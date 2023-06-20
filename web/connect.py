import psycopg2

connection = psycopg2.connect(
    user='test2',
    password='test',
    host='localhost',
    port='5432',
    database='test')
cursor = connection.cursor()