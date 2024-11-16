#Customer Details
from database import *

class Customer:
    def __init__(self, username, password, name, age, city, balance, account_number):
        self.__username = username
        self.__password = password
        self.__name = name
        self.__age = age
        self.__city = city
        self.balance = balance
        self.__account_number = account_number

    def createuser(self):
        db_query(f"INSERT INTO customers VALUES ('{self.__username}', '{self.__password}', '{self.__name}', '{self.__age}', '{self.__city}', '{self.__account_number}', 0 , '{self.__account_number}', 1  );")
        mydb.commit()
    
    @staticmethod
    def get_user_details(username):
        result = db_query(f"SELECT * FROM customers WHERE username = '{username}'")
        if result:
            return result[0]  # Return user details as a tuple
        return None
