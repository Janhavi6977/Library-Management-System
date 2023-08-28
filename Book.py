import Connection
from tabulate import tabulate
from datetime import datetime
from datetime import timedelta
from datetime import date
import time



def createBook():

    print('-------Register a new book in Library--------')
    print('')
    book_name = input('Please enter book name:')
    isbn = input('Please enter isbn:')
    year_published = int(input("Please enter publish year:"))
    author = input("Please enter author name:")
    publisher = input("Please enter publisher name:")
    quantity = int(input("Please enter books quantity:"))
    print('')
    sql = "INSERT INTO Book (book_name, isbn,year_published,author,publisher,quantity,available) VALUES (%s, %s, %s, " \
          "%s,%s,%s,%s) "
    val = (book_name, isbn, year_published, author, publisher, quantity, "Y")
    Connection.mycursor.execute(sql, val)
    rowcount = Connection.mycursor.rowcount
    Connection.mydb.commit()
    return rowcount


def displayAllBooks():
    sql = "SELECT * FROM Book"
    Connection.mycursor.execute(sql)
    result = Connection.mycursor.fetchall()
    return result


def modifyBook():
    try:
        bookDetails = displayAllBooks()
        print('')
        print(tabulate(bookDetails,
                       headers=['Book_Id', 'Book_Name', 'ISBN', 'Published Year', 'Author', 'Publisher', 'Quantity',
                                'Available'], tablefmt='psql'))
        print('')
        book_id = input("Enter book id to be edited : ")
        sql = "select * from book where book_id=" + book_id
        Connection.mycursor.execute(sql)
        res = Connection.mycursor.fetchall()
        if (len(res) == 0):
            print('')
            print("Sorry, this book does not exist in Library!")
            return
        for x in res:
            print('')
            print(tabulate(res,
                           headers=['Book_Id', 'Book_Name', 'ISBN', 'Year_published', 'Author', 'Publisher',
                                    'Quantity', 'Available'], tablefmt='psql'))
            print("")
        headers = [i[0] for i in Connection.mycursor.description]
        print('')
        inputs = [str(x) for x in input("Enter the comma separated field names which you want to modify :").split(',')]
        print('')
        print("\nThe values of input are", inputs)
        sql = "Update book set "
        count = 0
        for field in inputs:
            for x in headers:
                if (field.upper() == x.upper()):
                    count = 1
            if (count == 1):
                val = input("Enter new " + field + ": ")
                if ((val.isnumeric()) and (field.upper() != 'ISBN')):
                    sql += field + " = " + val + ","
                else:
                    sql += field + " = '" + val + "',"
                count = 0
            else:
                print('')
                print("Sorry, the field name " + field + " does not exist!")
                return
        sql = sql[:-1]
        sql += " where book_id=" + book_id
        Connection.mycursor.execute(sql)
        Connection.mydb.commit()
        print('')
        print("Book details for book id " + book_id + " has been updated successfully! ")
        print('')
        sql = "select * from book where book_id=" + book_id
        Connection.mycursor.execute(sql)
        res = Connection.mycursor.fetchall()
        for x in res:
            print('')
            print(tabulate(res,
                           headers=['Book_Id', 'Book_Name', 'ISBN', 'Year_published', 'Author', 'Publisher',
                                    'Quantity', 'Available'], tablefmt='psql'))
            print("")
    except Exception as e:
        print(e)
        return


def removeBook():
    try:
        bookDetails = displayAllBooks()
        print(tabulate(bookDetails,
                       headers=['Book_Id', 'Book_Name', 'ISBN', 'Published Year', 'Author', 'Publisher', 'Quantity',
                                'Available'], tablefmt='psql'))
        print('')
        book_id = input("Enter book id to be deleted : ")
        print('')
        sql = "select * from book where book_id="+book_id
        Connection.mycursor.execute(sql)
        res = Connection.mycursor.fetchall()
        if(len(res)==0):
            print('')
            print("Sorry, this book does not exist in Library!")
            return
        sql="select u.user_id,u.user_name,u.user_email,u.user_phone,bh.book_id, b.book_name,bh.issue_date," \
            "bh.return_date,bh.approved from bookhistory bh inner join user u on bh.user_id=u.user_id left " \
            "join book b on b.book_id=bh.book_id where bh.book_id="+book_id

        Connection.mycursor.execute(sql)
        res= Connection.mycursor.fetchall()

        if (len(res)==0):
            sql2="delete from book where book_id="+book_id
            Connection.mycursor.execute(sql2)
            Connection.mydb.commit()
            if ( Connection.mycursor.rowcount>0):
                print("Book has been successfully removed!")
                print('')
                bookDetails =displayAllBooks()
                print(tabulate(bookDetails,
                                headers=['Book_Id', 'Book_Name', 'ISBN', 'Published Year', 'Author', 'Publisher', 'Quantity',
                                    'Available'], tablefmt='psql'))
        else:
            for row in res:
                if (row[8]=="Y"):
                    currentDate = time.strptime(datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d")
                    returnDate = time.strptime(row[7].strftime('%Y-%m-%d'), "%Y-%m-%d")
                    if (returnDate>=currentDate):
                        print('')
                        print("Sorry,this book is already issued to "+row[1]+" with return date "+str(row[7]))
                        print('')
                        print("Kindly delete after the "+str(row[7])+" !")
                        print(' ')
                        print("Below are the issued book details:-")
                        print('')
                        print(tabulate (res,
                                        headers=['User_id','User_name','user_email','user_phone','book_id',
                                                 'book_name','book_issue_date','book_return_date','book_approved'],tablefmt='psql'))
                        
                    else:
                        print("below are the issued book details:-")
                        print(tabulate(res,
                                       headers=['User_id', 'User_name', 'user_email', 'user_phone', 'book_id'
                                                'book_name', 'book_issue_date', 'book_approved'], tablefmt='psql'))

                        print("This book was issued to" + row[1] + "but return date has expired")
                        bookDeleteFromHistoryAndBook(book_id)
                else:
                    bookDeleteFromHistoryAndBook(book_id)
            return
    except Exception as e:
        print(e)
def bookDeleteFromHistoryAndBook(book_id):
    print("")
    sql3="delete from BookHistory where book_id="+book_id
    Connection.mycursor.execute(sql3)
    sql4="delete from book where book_id="+book_id
    Connection.mycursor.execute(sql4)
    Connection.mydb.commit()
    print("Book has been removed successfully!")
    bookDetails = displayAllBooks()
    print(tabulate(bookDetails,
                   headers=['Book_Id', 'Book_Name', 'ISBN', 'Published Year', 'Author', 'Publisher', 'Quantity',
                            'Available'], tablefmt='psql'))


def displayIssuedBooks():
    sql = "select u.user_id,u.user_name,u.user_email,u.user_phone,bh.book_id," \
          "b.book_name,bh.issue_date,bh.return_date,bh.approved from bookhistory bh inner join user u " \
          "on bh.user_id=u.user_id left join book b on b.book_id=bh.book_id where bh.approved='Y'"
    Connection.mycursor.execute(sql)
    result = Connection.mycursor.fetchall()
    if (len(result)==0):
        print('')
        print("Sorry, Currently no books are issued!")
    else:
        print("Below are the issued book details:-")
        print('')
        print(tabulate(result,
                    headers=['User_id', 'User_name', 'User_email', 'User_phone', 'Book_id',
                            'Book_name',
                            'Book_Issue_date', 'Book_Return_Date',
                            'Book_Approved'], tablefmt='psql'))


def displayUnissuedBooks():
    sql = "select u.user_id,u.user_name,u.user_email,u.user_phone,bh.book_id," \
          "b.book_name,bh.issue_date,bh.return_date,bh.approved from bookhistory bh inner join user u " \
          "on bh.user_id=u.user_id left join book b on b.book_id=bh.book_id where bh.approved='N'"
    Connection.mycursor.execute(sql)
    result = Connection.mycursor.fetchall()
    if (len(result)==0):
        print("Sorry, no pending books are to be issued!")
    else:
        print("Below books are pending to be issued:-")
        print('')
        print(tabulate(result,
                    headers=['User_id', 'User_name', 'User_email', 'User_phone', 'Book_id',
                            'Book_name',
                            'Book_Issue_date', 'Book_Return_Date',
                            'Book_Approved'], tablefmt='psql'))

def displaybookhistoryrecords():
    sql = "SELECT * FROM Bookhistory"
    Connection.mycursor.execute(sql)
    result = Connection.mycursor.fetchall()
    return result

def approveUserRequest():
    try:
        sql = "select u.user_id,u.user_name,bh.book_id,b.book_name,bh.issue_date,bh.return_date,bh.approved " \
              "from bookhistory bh left join book b on " \
              "bh.book_id=b.book_id left join " \
              "user u on bh.user_id=u.user_id where exists (select * from bookhistory where approved='N')"
        Connection.mycursor.execute(sql)
        res = Connection.mycursor.fetchall()
        if (len(res)==0):
            print('')
            print("All the books are currently approved in the records!")
            print('')
            displayIssuedBooks()
            return
        print(tabulate(res,
                    headers=['user_id','user_name','book_id','book_name','issue_date','return_date','approved'], tablefmt='psql'))
        print("")
        book_id=input("Please enter book id which is to be approved: ")
        user_id=input("Please enter user id for which the book is to be approved: ")
        sql="select * from bookhistory where book_id="+book_id+" and user_id="+user_id
        Connection.mycursor.execute(sql)
        res = Connection.mycursor.fetchall()
        if (len(res) == 0):
            print('')
            print("Sorry, the combination of this book id and user id does not exist in the library!")
            return
        else:
            issueDate = datetime.now().strftime('%Y-%m-%d')
            returnDate = (datetime.now() + timedelta(days=12)).strftime('%Y-%m-%d')
            sqlUpdate = "Update bookhistory set issue_date= STR_TO_DATE('" + issueDate + "', '%Y-%m-%d'), " \
                        "return_date= STR_TO_DATE('" + returnDate + "', '%Y-%m-%d')" + " ,approved='Y' " \
                        "where book_id=" + book_id + " and user_id=" + user_id
            Connection.mycursor.execute(sqlUpdate)
            if (Connection.mycursor.rowcount>0):
                print('')
                print("Book with book_id="+book_id+" has been issued to the user with user_id="+user_id)
                displayIssuedBooks()
            else:
                print('')
                print("Sorry, this  book with book_id="+book_id+" could not be issued ")
        return
    except Exception as e:
        print(e)
        return





