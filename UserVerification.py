import Connection

def verifyUser():
        user_id = input('Please enter your id:')
        password = input('Please enter your password:')
        sql = "SELECT user_id,role FROM LoginDetails WHERE user_id=%s AND password=%s"
        val = (user_id,password)
        Connection.mycursor.execute(sql, val)
        result = Connection.mycursor.fetchall()
        return result

    #if(len(result)==1):
        #for row in result:
            #role = row[1]
        #return role