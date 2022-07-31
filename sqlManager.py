import mysql.connector as sql

mydb = sql.connect(host='localhost', user='root', passwd='07022109Ju+')
print('conexão estabelecida')

cursor = mydb.cursor()

cursor.execute()

