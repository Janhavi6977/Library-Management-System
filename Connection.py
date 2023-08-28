import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",

  database="library_management"
)
mycursor = mydb.cursor()






