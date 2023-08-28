import Connection
from tabulate import tabulate


def createUser():

    print('-------Register a new user--------')
    print('')
    user_name = input('Please enter user name:')
    user_address = input('Please enter user address:')
    user_email = input('Please enter user email:')
    user_phone = input('Please enter user phone:')
    try:
        sql = "INSERT INTO user (user_name, user_address,user_email,user_phone) " \
              "VALUES (%s, %s, %s, %s)"
        val = (user_name, user_address, user_email, user_phone)
        Connection.mycursor.execute(sql, val)
        rowcount = Connection.mycursor.rowcount
        if rowcount > 0:
            sql = "select user_id,user_name,user_address,user_email,user_phone from user where user_email='" + user_email + "'"
            Connection.mycursor.execute(sql)
            result = Connection.mycursor.fetchall()
            print('')
            print("Below user details have been added successfully!")
            print('')
            print(tabulate(result,
                           headers=['User_id', 'User_name', 'User_address', 'User_email', 'User_phone'],
                           tablefmt='psql'))
            user_id = 1;
            for row in result:
                user_id = row[0]

            sql = "INSERT INTO LoginDetails (user_id,password,role) VALUES (%s,%s,%s)"
            val = (user_id, "password", "user")
            resultCount = Connection.mycursor.execute(sql, val)
            Connection.mydb.commit()
    except Exception as e:
        print(e)
        return




def displayAllUserDetails():
    sql = "SELECT * FROM User"
    Connection.mycursor.execute(sql)
    result = Connection.mycursor.fetchall()
    return result


def modifyUserDetails():
    try:
        userdetails=displayAllUserDetails()
        print('')
        print(tabulate(userdetails,
                       headers=['user_id', 'user_name', 'user_address', 'user_email', 'user_phone'], tablefmt='psql'))
        print('')
        user_id = input("Enter user id to be edited : ")
        print('')
        sql = "select * from User where user_id=" + user_id
        Connection.mycursor.execute(sql)
        res = Connection.mycursor.fetchall()
        if len(res) == 0:
            print('')
            print("Sorry, this user does not exist in Library!")
            return
        for x in res:
            print('')
            print(tabulate(res,
                           headers=['user_id', 'user_name', 'user_address', 'user_email', 'user_phone'],
                           tablefmt='psql'))
            print("")
        headers = [i[0] for i in Connection.mycursor.description]
        inputs = [str(x) for x in input("Enter the comma separated field names which you want to modify :").split(',')]
        print('')
        print("\nThe values of input are", inputs)
        sql = "Update User set "
        count = 0
        for field in inputs:
            for x in headers:
                if field.upper() == x.upper():
                    count = 1
            if count == 1:
                print('')
                val = input("Enter new " + field + ": ")
                if (val.isnumeric()) and (field.upper() != 'USER_PHONE'):
                    sql += field + " = " + val + ","
                else:
                    sql += field + " = '" + val + "',"
                count = 0
            else:
                print('')
                print("Sorry, the field name " + field + " does not exist!")
                return
        sql = sql[:-1]
        sql += " where user_id=" + user_id
        Connection.mycursor.execute(sql)
        Connection.mydb.commit()
        print('')
        print("User details for user id " + user_id + " has been updated successfully! ")
        print('')
        sql = "select * from User where user_id=" + user_id
        Connection.mycursor.execute(sql)
        res = Connection.mycursor.fetchall()
        for _ in res:
            print(tabulate(res,
                           headers=['user_id', 'user_name', 'user_address', 'user_email', 'user_phone'],
                           tablefmt='psql'))
            print("")
    except Exception as e:
        print(e)
        return


def displayAllAvailableBooks():
    sql = "SELECT * FROM Book where available='Y'"
    Connection.mycursor.execute(sql)
    result = Connection.mycursor.fetchall()
    return result


def displayIssuedBooks(user_id):
    sql = "SELECT u.user_name,u.user_phone,u.user_email,u.user_address ,b.book_name,bh.issue_date,bh.return_date," \
          " b.isbn, b.year_published,b.author,b.publisher from bookhistory bh inner join " \
          "book b on bh.book_id=b.book_id left join user u on u.user_id=bh.user_id where bh.approved='Y' and " \
          "bh.user_id="+str(user_id)
    Connection.mycursor.execute(sql)
    result = Connection.mycursor.fetchall()
    if len(result)==0:
        print ("Sorry no book issued to this user id!")
        print("#######################")
    return result

def issueNewBook(user_id):
    print("Below are the available books:-")
    print('')
    bookDetails =displayAllAvailableBooks()
    print(tabulate(bookDetails,
                   headers=['Book_Id', 'Book_Name', 'ISBN', 'Published Year', 'Author', 'Publisher',
                            'Quantity', 'Available'], tablefmt='psql'))
    try:
        print('')
        book_id=input("enter book_id to be issued:")
        sql = "select * from book where book_id=" + book_id
        Connection.mycursor.execute(sql)
        res = Connection.mycursor.fetchall()
        if len(res) == 0:
            print('')
            print("Sorry, this book does not exist in Library!")
            return
        else:
            sql="INSERT INTO Bookhistory(book_id,user_id,approved) values(%s,%s,%s)"
            val = (book_id,user_id,"N")
            Connection.mycursor.execute(sql, val)
            Connection.mydb.commit()
            rowcount = Connection.mycursor.rowcount
            if rowcount>0:
                print('')
                print("Kindly get the book approved by the admin!!")
            else:
                print('')
                print("Sorry the credentials entered are wrong!!")
    except Exception as e:
        print(e)
        return




