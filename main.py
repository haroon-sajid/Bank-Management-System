from register import *
from bank import *
import tkinter as tk
from tkinter import messagebox
from register import SignUp, SignIn
from bank import Bank, db_query, mydb
from tkinter import PhotoImage, messagebox

class BankingApp:
    def __init__(self, window):
        self.master = window
        self.master.geometry("700x500")
        self.master.configure(bg="#023047")
        window.title("Welcome to Haroon Banking")
        # Set icon and background
        p1 = PhotoImage(file='./images/bank.png')
        window.iconphoto(True, p1)
        window.configure(background="#023047")
        self.user = None
        self.account_number = None
         # Header with blue background
        self.header = tk.Label(window, text="Welcome to Haroon Banking", background="#1b5789",
                               foreground="white", font=("Arial", 18, "bold"))
        self.header.pack(fill="x", pady=(20, 0))

        # Main canvas
        self.Canvas1 = tk.Canvas(window, background="#e0e0e0", borderwidth="0", relief="ridge")
        self.Canvas1.place(relx=0.15, rely=0.20, relheight=0.7, relwidth=0.7)
        self.show_main_screen()

    def show_main_screen(self):
        """Displays the main menu for Sign In and Sign Up."""
        self.clear_window()
        # Set the main background color for the canvas
        self.master.configure(bg="#023047")
        # Define hover functions
        def on_enter(event):
            event.widget.configure(bg="#fb941d")  # Darker shade on hover

        def on_leave(event):
            event.widget.configure(bg="#1b5789")  # Original shade when not hovering

        # Banner Label at the top
        tk.Label(self.master, text="Welcome to Haroon Banking System", font=("Arial", 16, "bold"),
                 bg="#fb941d", fg="white", padx=20, pady=5).pack(pady=40)

        # Create a white frame to act as a container (the "box") for the buttons
        button_frame = tk.Frame(self.master, bg="white", padx=100, pady=60)
        button_frame.pack(pady=10)

        # Sign In Button inside the frame
        sign_in_button = tk.Button(button_frame, text="Sign In", font=("Arial", 12), bg="#1b5789", fg="white", 
                                   command=self.sign_in)
        sign_in_button.pack(pady=15)
        sign_in_button.bind("<Enter>", on_enter)  # Bind hover enter event
        sign_in_button.bind("<Leave>", on_leave)  # Bind hover leave event

        # Sign Up Button inside the frame
        sign_up_button = tk.Button(button_frame, text="Sign Up", font=("Arial", 12), bg="#1b5789", fg="white", 
                                   command=self.sign_up)
        sign_up_button.pack(pady=15)
        sign_up_button.bind("<Enter>", on_enter)  # Bind hover enter event
        sign_up_button.bind("<Leave>", on_leave)  # Bind hover leave event



    def sign_in(self):
        """Sign In screen."""
        self.clear_window()
        tk.Label(self.master, text="Sign In", font=("Arial", 14, "bold"), bg="#023047", fg="white").pack(pady=20)
        tk.Label(self.master, text="Username:", font=("Arial", 12), bg="#023047", fg="white").pack()
        username_entry = tk.Entry(self.master, width=30)
        username_entry.pack(pady=5)

        tk.Label(self.master, text="Password:", font=("Arial", 12), bg="#023047", fg="white").pack()
        password_entry = tk.Entry(self.master, width=30, show="*")
        password_entry.pack(pady=5)


        def process_sign_in():
            username = username_entry.get()
            password = password_entry.get()

            # Check if username exists in the database
            user_data = db_query(f"SELECT account_number, status FROM customers WHERE username = '{username}'")

            if user_data:  # If user_data is not empty, username exists
                account_number, status = user_data[0]  # Extract the account number and status
                
                if status == 0:  # Check if account is marked as deleted
                    messagebox.showerror("Error", "This account has been deleted. Please contact support.")
                    return
                
                if SignIn(username, password):  # Validate credentials
                    self.user = username
                    self.account_number = account_number
                    messagebox.showinfo("Success", "Sign In Successful!")
                    self.show_services_screen()
                else:
                    messagebox.showerror("Error", "Invalid password. Please try again.")
            else:
                messagebox.showerror("Error", "Username not found. Please register first.")

        tk.Button(self.master, text="Submit", font=("Arial", 12), bg="#1b5789", fg="white", 
                command=process_sign_in).pack(pady=10)
        tk.Button(self.master, text="Back", font=("Arial", 12), bg="#fb941d", fg="white", 
                command=self.show_main_screen).pack(pady=5)

    def sign_up(self):
        """Sign Up screen."""
        self.clear_window()
        tk.Label(self.master, text="Sign Up", font=("Arial", 14, "bold"), bg="#023047", fg="white").pack(pady=20)

        fields = ["Username", "Password", "Full Name", "Age", "City"]
        entries = {}
        for field in fields:
            tk.Label(self.master, text=f"{field}:", font=("Arial", 12), bg="#023047", fg="white").pack()
            entry = tk.Entry(self.master, width=30)
            entry.pack(pady=5)
            entries[field] = entry

        def process_sign_up():
            data = {field: entry.get() for field, entry in entries.items()}
            if all(data.values()):
                if SignUp(data["Username"], data["Password"], data["Full Name"], data["Age"], data["City"]):
                    messagebox.showinfo("Success", "Sign Up Successful!")
                    self.show_main_screen()
                else:
                    messagebox.showerror("Error", "Username already exists. Try a different one.")
            else:
                messagebox.showerror("Error", "Please fill in all fields.")

        tk.Button(self.master, text="Submit", font=("Arial", 12), bg="#1b5789", fg="white", 
                  command=process_sign_up).pack(pady=10)
        tk.Button(self.master, text="Back", font=("Arial", 12), bg="#fb941d", fg="white", 
                  command=self.show_main_screen).pack(pady=5)

    def show_services_screen(self):
        """Displays the banking services screen."""
        self.clear_window()
        tk.Label(self.master, text=f"Welcome, {self.user.capitalize()}", font=("Arial", 14, "bold"),
                 bg="#023047", fg="white").pack(pady=20)

        services = [
            ("Balance Enquiry", self.balance_enquiry),
            ("Deposit Cash", self.cash_deposit),
            ("Withdraw Cash", self.cash_withdraw),
            ("Fund Transfer", self.fund_transfer),
            ("Exit", self.exit_application)
        ]

        for service, command in services:
            tk.Button(self.master, text=service, font=("Arial", 12), bg="#1b5789", fg="white", 
                      command=command).pack(pady=5)

    def balance_enquiry(self):
        try:
            # Ensure Bank class is initialized correctly
            bobj = Bank(self.user, self.account_number)
            # Call balance inquiry and get the balance
            balance = bobj.balanceequiry()  # This will now return the balance

            # Clear the current window content
            self.clear_window()

            # Display the balance directly on the current window
            tk.Label(self.master, text="Balance Enquiry", font=("Arial", 14, "bold"), bg="#023047", fg="white").pack(pady=20)
            tk.Label(self.master, text=f"Your current balance is: {balance}", font=("Arial", 12), bg="#023047", fg="white").pack(pady=20)

            # Button to go back to the services screen
            tk.Button(self.master, text="Back", font=("Arial", 12), bg="#fb941d", fg="white", command=self.show_services_screen).pack(pady=10)

        except Exception as e:
            # Handle unexpected errors and display them to the user
            messagebox.showerror("Error", f"An error occurred while fetching balance: {str(e)}")


    def show_services_screen(self):
        """Displays the banking services screen."""
        self.clear_window()
        tk.Label(self.master, text=f"Welcome, {self.user.capitalize()}", font=("Arial", 14, "bold"),
                bg="#023047", fg="white").pack(pady=20)

        services = [
        ("Balance Enquiry", self.balance_enquiry),
        ("Deposit Cash", self.cash_deposit),
        ("Withdraw Cash", self.cash_withdraw),
        ("Fund Transfer", self.fund_transfer),
        ("View Account Details", self.display_account_details),
        ("View Transaction History", self.display_transaction_history),
        ("Delete Account", self.delete_account),  # Add this line
        ("Exit", self.exit_application)
    ]


        for service, command in services:
            tk.Button(self.master, text=service, font=("Arial", 12), bg="#1b5789", fg="white", 
                    command=command).pack(pady=5)

    def display_account_details(self):
        """Displays account details like name, account number, and balance on the same window."""
        try:
            # Get the account details
            bobj = Bank(self.user, self.account_number)
            account_info = bobj.account_details()  # You need to define this method in the Bank class
            if account_info:
                self.clear_window()  # Clear current window before showing account details
                tk.Label(self.master, text="Account Details", font=("Arial", 14, "bold"), bg="#023047", fg="white").pack(pady=20)
                tk.Label(self.master, text=f"Name: {account_info['name']}", font=("Arial", 12), bg="#023047", fg="white").pack(pady=5)
                tk.Label(self.master, text=f"Account Number: {account_info['account_number']}", font=("Arial", 12), bg="#023047", fg="white").pack(pady=5)
                tk.Label(self.master, text=f"Balance: {account_info['balance']}", font=("Arial", 12), bg="#023047", fg="white").pack(pady=5)
                # Back Button to go back to services screen
                tk.Button(self.master, text="Back", font=("Arial", 12), bg="#fb941d", fg="white", command=self.show_services_screen).pack(pady=10)
            else:
                messagebox.showerror("Error", "Account not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")


    def display_transaction_history(self):
        """Displays transaction history of the user on the same window."""
        try:
            # Get the transaction history
            bobj = Bank(self.user, self.account_number)
            transactions = bobj.transaction_history()  # You need to define this method in the Bank class
            if transactions:
                self.clear_window()  # Clear current window before showing transaction history
                tk.Label(self.master, text="Transaction History", font=("Arial", 14, "bold"), bg="#023047", fg="white").pack(pady=20)
                history_text = "\n".join([f"{txn[0]} - {txn[1]}: {txn[2]}" for txn in transactions])
                tk.Label(self.master, text=history_text, font=("Arial", 10), justify="left", bg="#023047", fg="white").pack(pady=10)
                # Back Button to go back to services screen
                tk.Button(self.master, text="Back", font=("Arial", 12), bg="#fb941d", fg="white", command=self.show_services_screen).pack(pady=10)
            else:
                messagebox.showinfo("No Transactions", "No transactions found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")



    def cash_deposit(self):
        self.transaction_screen("Deposit", lambda amount: self.process_transaction("deposit", amount))

    def cash_withdraw(self):
        self.transaction_screen("Withdraw", lambda amount: self.process_transaction("withdraw", amount))

    def fund_transfer(self):
        self.transaction_screen("Transfer", lambda amount: self.process_transaction("transfer", amount, is_transfer=True))

    def transaction_screen(self, action, process_func):
        """Screen for deposit, withdrawal, and fund transfer."""
        self.clear_window()
        tk.Label(self.master, text=f"{action} Amount", font=("Arial", 14, "bold"), bg="#023047", fg="white").pack(pady=20)

        tk.Label(self.master, text="Enter Amount:", font=("Arial", 12), bg="#023047", fg="white").pack()
        amount_entry = tk.Entry(self.master, width=30)
        amount_entry.pack(pady=5)

        if action == "Transfer":
            tk.Label(self.master, text="Enter Receiver's Account Number:", font=("Arial", 12), bg="#023047", fg="white").pack()
            receiver_entry = tk.Entry(self.master, width=30)
            receiver_entry.pack(pady=5)

        def submit_action():
            try:
                amount = int(amount_entry.get())
                if action == "Transfer":
                    receiver = int(receiver_entry.get())
                    process_func((amount, receiver))
                else:
                    process_func(amount)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")

        tk.Button(self.master, text="Submit", font=("Arial", 12), bg="#1b5789", fg="white", 
                  command=submit_action).pack(pady=10)
        tk.Button(self.master, text="Back", font=("Arial", 12), bg="#fb941d", fg="white", 
                  command=self.show_services_screen).pack(pady=5)


    def process_transaction(self, action, amount, is_transfer=False):
        bobj = Bank(self.user, self.account_number)
        try:
            if action == "deposit":
                bobj.deposit(amount)
                messagebox.showinfo("Success", "Deposit Successful!")
            
            elif action == "withdraw":
                # Check if the withdrawal amount is less than or equal to the balance
                current_balance = bobj.balanceequiry()
                if amount > current_balance:
                    messagebox.showerror("Error", "Insufficient Balance. Please enter a smaller amount.")
                    return
                bobj.withdraw(amount)
                messagebox.showinfo("Success", "Withdrawal Successful!")
            
            elif is_transfer:
                receiver, amount = amount
                # Check if the sender has enough funds for the transfer
                sender_balance = bobj.balanceequiry()
                if amount > sender_balance:
                    messagebox.showerror("Error", "Insufficient Balance. Please enter a smaller amount.")
                    return
                # Check if the receiver exists
                receiver_data = db_query(f"SELECT account_number FROM customers WHERE account_number = {receiver}")
                if not receiver_data:
                    messagebox.showerror("Error", "Receiver's account does not exist.")
                    return
                bobj.fundtransfer(receiver, amount)
                messagebox.showinfo("Success", "Transfer Successful!")
            
            mydb.commit()
            self.show_services_screen()
        
        except Exception as e:
            messagebox.showerror("Error", str(e))



    def delete_account(self):
        """Marks the user's account as deleted by updating the status to 0."""
        try:
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete your account?")
            if confirm:
                db_query(f"UPDATE customers SET status = 0 WHERE username = '{self.user}';")
                mydb.commit()
                messagebox.showinfo("Account Deleted", "Your account has been successfully deleted.")
                self.user = None
                self.account_number = None
                self.show_main_screen()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting account: {str(e)}")

            

    def exit_application(self):
        self.master.destroy()

    def clear_window(self):
        """Clears the current window."""
        for widget in self.master.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()
