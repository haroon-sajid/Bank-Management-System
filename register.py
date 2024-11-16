#User Registration Signin Signup
from customer import *
from bank import Bank
import random


def SignUp(username, password, name, age, city):
    temp = db_query(f"SELECT username FROM customers where username = '{username}';")
    if temp:
        return False  # Username exists
    else:
        account_number = random.randint(10000000, 99999999)
        cobj = Customer(username, password, name, age, city, account_number)
        cobj.createuser()
        bobj = Bank(username, account_number)
        bobj.create_transaction_table()
        return True

def SignIn(username, password):
    temp = db_query(f"SELECT username, password FROM customers where username = '{username}';")
    if temp and temp[0][1] == password:
        return True
    return False
