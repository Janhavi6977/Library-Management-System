from tabulate import tabulate
import User
import UserVerification
import Book
if __name__ == '__main__':
    print('')
    print("------WELCOME TO THE 24/7 LIBRARY--------")
    print('')
    print('-------Library Management System---------')
    print('')
    ch = "Y"
    while ch == "Y":
        print('Login')
        result = UserVerification.verifyUser()
        if (len(result)==0):
            print('')
            print("Incorrect user_id or password. Please try again!")
            print("#############################")
            print('')
        else:
            for row in result:
                user_id=row[0]
                role=row[1]
            if(role == "admin"):
                print('')
                print("Below is list of menus you can work on :-")
                print('')
                while ch == "Y":
                    print("1. Display all book details")
                    print("2. Display all issued book details")
                    print("3. Display unissued book details")
                    print("4. Register a new book in library")
                    print("5. Modify book details")
                    print("6. Remove book")
                    print("7. Register User Details")
                    print("8. Display all user details")
                    print("9. Modify User details")
                    print("10. Approve the book requested by user")
                    print("11. Logout")
                    print("12. Exit")
                    print('')
                    choice = int(input("Enter your choice:"))
                    if(choice == 1):
                        print('')
                        bookDetails = Book.displayAllBooks()
                        print(tabulate(bookDetails, headers=['Book_Id', 'Book_Name','ISBN','Published Year','Author','Publisher','Quantity','Available'], tablefmt='psql'))
                    elif(choice == 2):
                        print('')
                        Book.displayIssuedBooks()
                    elif (choice == 3):
                        print('')
                        Book.displayUnissuedBooks()
                    elif(choice == 4):
                        print('')
                        bookCreateCount = Book.createBook()
                        if(bookCreateCount >0):
                            print("Book has been registered successfully!")
                            print('')
                            bookDetails = Book.displayAllBooks()
                            print(tabulate(bookDetails,
                                           headers=['Book_Id', 'Book_Name', 'ISBN', 'Published Year', 'Author', 'Publisher',
                                                    'Quantity', 'Available'], tablefmt='psql'))
                    elif (choice == 5):
                        print('')
                        Book.modifyBook()
                    elif (choice == 6):
                        print('')
                        Book.removeBook()
                    elif (choice == 7):
                        print('')
                        User.createUser();
                    elif (choice == 8):
                        print('')
                        userdetails=User.displayAllUserDetails()
                        print(tabulate(userdetails,
                                       headers=['user_id', 'user_name', 'user_address', 'user_email', 'user_phone'], tablefmt='psql'))
                    elif (choice == 9):
                        print('')
                        User.modifyUserDetails()
                    elif (choice == 10):
                        print('')
                        Book.approveUserRequest()
                    elif (choice == 11):
                        print('')
                        print("You have logged out from your account!")
                        print("##########################")
                        print('')
                        break
                    else:
                        print('')
                        print("THANK YOU FOR VISITING 24/7 LIBRARY")
                        print('')
                        print("  -----XXXX-----XXXX----XXX-----")
                        print('')
                        exit(0)
                    print('')
                    ch = input("Do You Want to Continue <y/n>:")
                    print('')
                    print("Below is list of menus you can work on :-")
                    print('')
                    ch = ch.upper()
                    if(ch=="N"):
                        print('')
                        print("THANK YOU FOR VISITING 24/7 LIBRARY")
                        print('')
                        print("  -----XXXX-----XXXX----XXX-----")
                        print('')
                        break
            elif(role == "user"):
                while ch == "Y":
                    print('')
                    print("Below is list of menus you can work on :-")
                    print('')
                    print("1. Display Available Book Details")
                    print("2. Check Issued Book Details")
                    print("3. Request to issue a new book")
                    print("4. Logout")
                    print("5. Exit")
                    print('')
                    choice = int(input("Enter your choice:"))
                    if(choice == 1):
                        print('')
                        bookDetails=User.displayAllAvailableBooks()
                        print(tabulate(bookDetails,
                                       headers=['Book_Id', 'Book_Name', 'ISBN', 'Published Year', 'Author', 'Publisher',
                                                'Quantity', 'Available'], tablefmt='psql'))
                    elif(choice == 2):
                        print('')
                        issuedBooks=User.displayIssuedBooks(user_id)
                        if (len(issuedBooks)>0):
                            print(tabulate(issuedBooks,
                                       headers=['user_Name','user_phone','user_email','user_address' ,'book_name','issue_date','return_date'," \
                                                " 'isbn', 'year_published','author','publisher'], tablefmt='psql'))
                    elif(choice == 3):
                        print('')
                        issuebook=User.issueNewBook(user_id)
                    elif (choice == 4):
                        print('')
                        print("You have logged out from your account!")
                        print("##########################")
                        print('')
                        break
                else:
                    exit(0)
                ch = input("Do You Want to Continue <y/n>:")
                print('')
                ch = ch.upper()
                if(ch=="N"):
                    print('')
                    print("THANK YOU FOR VISITING 24/7 LIBRARY")
                    print('')
                    print("  -----XXXX-----XXXX----XXX-----")
                    print('')
                    break
            else:
                print('User id and password are incorrect, please retry!')
                print('###################################')