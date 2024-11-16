from database import *
import datetime

class Bank:
    def __init__(self, username, account_number):
        self.__username = username
        self.__account_number = account_number

    def create_transaction_table(self):
        db_query(f"CREATE TABLE IF NOT EXISTS {self.__username}_transaction "
                 f"( timedate VARCHAR(30),"
                 f"account_number INTEGER,"
                 f"remarks VARCHAR(30),"
                 f"amount INTEGER )")

    # Method to view account details (name, account number, balance)
    def account_details(self):
        try:
            # Fetch user details from the database
            user_details = db_query(f"SELECT name, account_number, balance FROM customers WHERE username = '{self.__username}';")
            if user_details:
                # Unpack the first tuple in the result
                name, account_number, balance = user_details[0]
                return {
                    'name': name,
                    'account_number': account_number,
                    'balance': balance
                }
            else:
                return None
        except Exception as e:
            raise Exception(f"Error fetching account details: {str(e)}")


    # Method to fetch transaction history
    def transaction_history(self):
        try:
            # Fetch transaction history from the user's transaction table
            transactions = db_query(f"SELECT timedate, remarks, amount FROM {self.__username}_transaction;")
            if transactions:
                return transactions
            else:
                return []
        except Exception as e:
            raise Exception(f"Error fetching transaction history: {str(e)}")

    def balanceequiry(self):
        try:
            # Query the balance from the database
            temp = db_query(f"SELECT balance FROM customers WHERE username = '{self.__username}';")
            if temp:
                balance = temp[0][0]
                return balance  # Return the balance instead of printing it
            else:
                return 0  # Return 0 if no balance is found
        except Exception as e:
            raise Exception(f"Error fetching balance: {str(e)}")

    def deposit(self, amount):
        temp = db_query(f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        test = amount + temp[0][0]
        db_query(f"UPDATE customers SET balance = '{test}' WHERE username = '{self.__username}'; ")
        self.balanceequiry()
        db_query(f"INSERT INTO {self.__username}_transaction VALUES ("
                 f"'{datetime.datetime.now()}',"
                 f"'{self.__account_number}',"
                 f"'Amount Deposit',"
                 f"'{amount}'"
                 f")")
        print(f"{self.__username} Amount is Sucessfully Deposited into Your Account {self.__account_number}")


    def withdraw(self, amount):
        temp = db_query(
            f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        if amount > temp[0][0]:
            print("Insufficient Balance Please Deposit Money")
        else:
            test = temp[0][0] - amount
            db_query(
                f"UPDATE customers SET balance = '{test}' WHERE username = '{self.__username}'; ")
            self.balanceequiry()
            db_query(f"INSERT INTO {self.__username}_transaction VALUES ("
                     f"'{datetime.datetime.now()}',"
                     f"'{self.__account_number}',"
                     f"'Amount Withdraw',"
                     f"'{amount}'"
                     f")")
            print(
                f"{self.__username} Amount is Sucessfully Withdraw from Your Account {self.__account_number}")

    def fundtransfer(self, receive, amount):
        temp = db_query(
            f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        if amount > temp[0][0]:
            print("Insufficient Balance Please Deposit Money")
        else:
            temp2 = db_query(
                f"SELECT balance FROM customers WHERE account_number = '{receive}';")
            if temp2 == []:
                print("Account Number Does not Exists")
            else:
                test1 = temp[0][0] - amount
                test2 = amount + temp2[0][0]
                db_query(
                    f"UPDATE customers SET balance = '{test1}' WHERE username = '{self.__username}'; ")
                db_query(
                    f"UPDATE customers SET balance = '{test2}' WHERE account_number = '{receive}'; ")
                receiver_username = db_query(
                    f"SELECT username FROM customers where account_number = '{receive}';")
                self.balanceequiry()
                db_query(f"INSERT INTO {receiver_username[0][0]}_transaction VALUES ("
                         f"'{datetime.datetime.now()}',"
                         f"'{self.__account_number}',"
                         f"'Fund Transfer From {self.__account_number}',"
                         f"'{amount}'"
                         f")")
                db_query(f"INSERT INTO {self.__username}_transaction VALUES ("
                         f"'{datetime.datetime.now()}',"
                         f"'{self.__account_number}',"
                         f"'Fund Transfer -> {receive}',"
                         f"'{amount}'"
                         f")")
                print(
                    f"{self.__username} Amount is Sucessfully Transaction from Your Account {self.__account_number}")
