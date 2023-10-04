import random
import json

# Constants
MIN_DEPOSIT_AMOUNT = 50
PIN_LENGTH = 4
TAX_RATE = 0.01
MAX_LOGIN_ATTEMPTS = 3

# Data storage
user_data = []

def save_user_data():
    """Save user data to a plain text file."""
    with open("users.txt", "w") as file:
        for user_info in user_data:
            json.dump(user_info, file)
            file.write('\n')

def load_user_data():
    """Load user data from a plain text file."""
    try:
        with open("users.txt", "r") as file:
            lines = file.readlines()
            return [json.loads(line.strip()) for line in lines]
    except FileNotFoundError:
        return []

def create_account():
    """Create a new user account."""
    name = input("Enter your Name: ")
    
    while True:
        try:
            deposit = int(input(f"Please enter the deposit amount (should be more than {MIN_DEPOSIT_AMOUNT}): "))
            if deposit > MIN_DEPOSIT_AMOUNT:
                break
            else:
                print("Invalid input. The deposit amount should be more than 50.")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

    while True:
        pin = input(f"Please Enter {PIN_LENGTH}-digit pin code: ")
        if len(pin) == PIN_LENGTH and pin.isdigit():
            break
        else:
            print(f"Invalid Input. Your Pin should be {PIN_LENGTH} digits long.")

    user_id = random.randint(1000000000, 9999999999)
    username = name + str(random.randint(1, 100))
    print(f"User ID:{user_id}")
    print(f"Username:{username}")

    user_info = {
        "ID": user_id,
        "Name": name,
        "Username": username,
        "Pin_Code": pin,
        "Status": "Active",
        "Balance_Amount": deposit,
        "Currency": "PKR",
        "Statement": [{"Deposited of PKR": deposit}]
    }

    user_data.append(user_info)
    save_user_data()
    print(f"Account created successfully.")

def login(username, entered_pin):
    """Perform user login and return user information if successful."""
    for user_info in user_data:
        if user_info["Username"] == username and user_info["Pin_Code"] == entered_pin:
            return user_info
    return None
def find_user(username):
    """Find and return user information by username."""
    for user_info in user_data:
        if user_info["Username"] == username:
            return user_info
    return None

def checkin():
    """User login and account management."""
    username = input("Enter your username: ")
    user_info = find_user(username)

    if user_info is None:
        print("User not found. Please enter a valid username.")
        return None

    login_attempts = 0

    while login_attempts < MAX_LOGIN_ATTEMPTS:
        entered_pin = input("Enter your pin code: ")
        if login(username, entered_pin):
            print("You have logged in.")
            return user_info
        else:
            login_attempts += 1
            remaining_attempts = MAX_LOGIN_ATTEMPTS - login_attempts
            if remaining_attempts > 0:
                print(f"Invalid pin code. You have {remaining_attempts} attempt(s) left.")
            else:
                print("Your account has been blocked.")
                user_info["Status"] = "Blocked"
                save_user_data()
                return None

    return None

def account_detail(user_info):
    """Display user account details."""
    if user_info is None:
        print("You must be logged in to see your account details.")
        return
    print(f"Name: {user_info['Name']}")
    print(f"Username: {user_info['Username']}")
    print(f"Status: {user_info['Status']}")
    print(f"Balance: {user_info['Balance_Amount']}")

def deposit(user_info):
    """Perform a deposit transaction."""
    if user_info is None:
        print("You must be logged in to deposit.")
        return

    while True:
        try:
            deposit_amount = int(input(f"Please enter the deposit amount (should be more than {MIN_DEPOSIT_AMOUNT}): "))
            if deposit_amount > MIN_DEPOSIT_AMOUNT:
                break
            else:
                print(f"Invalid input. The deposit amount should be more than {MIN_DEPOSIT_AMOUNT}.")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

    current_balance = user_info["Balance_Amount"]
    new_balance = current_balance + deposit_amount
    user_info["Balance_Amount"] = new_balance
    user_info["Statement"].append({"Deposited of PKR": deposit_amount})
    save_user_data()
    print(f"Deposit of {deposit_amount} successfully added. New balance: {new_balance}")

def withdraw(user_info):
    """Perform a withdrawal transaction."""
    if user_info is None:
        print("You must be logged in to withdraw.")
        return

    if user_info["Status"] == "Blocked":
        print("Your account is blocked. Withdrawal is not allowed.")
        return

    while True:
        try:
            withdrawal_amount = int(input("Enter the withdrawal amount: "))
            if withdrawal_amount > 0:
                break
            else:
                print("Invalid input. Withdrawal amount must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

    current_balance = user_info["Balance_Amount"]

    if withdrawal_amount <= current_balance:
        tax = withdrawal_amount * TAX_RATE
        total_withdrawal = withdrawal_amount + tax

        if total_withdrawal <= current_balance:
            user_info["Balance_Amount"] = current_balance - total_withdrawal
            user_info["Statement"].append({"Withdrawal of PKR": withdrawal_amount})
            save_user_data()
            print(f"Withdrawal of PKR {withdrawal_amount} successful.")
            print(f"Tax deducted: PKR {tax}")
        else:
            print("Insufficient Balance!")
    else:
        print("Insufficient Balance!")

def update_pin(user_info):
    """Update the user's PIN."""
    if user_info is None:
        print("You must be logged in to update your PIN.")
        return
    current_pin = user_info["Pin_Code"]
    entered_pin = input("Enter your current pin code: ")

    if entered_pin == current_pin:
        while True:
            new_pin = input(f"Enter your new {PIN_LENGTH}-digit pin code: ")
            if len(new_pin) == PIN_LENGTH and new_pin.isdigit():
                user_info["Pin_Code"] = new_pin
                save_user_data()
                print("Pin code updated successfully.")
                break
            else:
                print(f"Invalid Input. Your Pin should be {PIN_LENGTH} digits long.")
    else:
        print("Incorrect pin code. Pin code updation failed.")

def check_statement(user_info):
    """Generate and display the user's account statement."""
    if user_info is None:
        print("You must be logged in to check your statement.")
        return
    user_id = user_info["ID"]
    with open(f"userstatement.txt", "w") as statement_file:
        statement_file.write(f"User ID: {user_id}\n")
        statement_file.write("Statement:\n")
        for entry in user_info["Statement"]:
            for key, value in entry.items():
                statement_file.write(f"{key}: {value}\n")
        print("Statement Generated Successfully!")


#Main program execution
user_data.extend(load_user_data())

while True:
    print("***Welcome***")
    print("MAIN MENU:\n1. Create Account\n2. Checkin\n3. Exit")
    user_choice = input("Please choose between (1/2/3): ").strip()
    if user_choice == "1":
        create_account()
    elif user_choice == "2":
        logged_in_user = checkin()
        while True:
                print("SUB-MENU:\n1. Account Detail\n2. Deposit\n3. Withdraw\n4. Update pin\n5. Check Statement\n6. Logout")
                sub_menu_choice = input("Please choose between (1/2/3/4/5/6): ").strip()
                if sub_menu_choice == "1":
                    account_detail(logged_in_user)
                elif sub_menu_choice == "2":
                    deposit(logged_in_user)
                elif sub_menu_choice == "3":
                    withdraw(logged_in_user)
                elif sub_menu_choice == "4":
                    update_pin(logged_in_user)
                elif sub_menu_choice == "5":
                    check_statement(logged_in_user)
                elif sub_menu_choice == "6":
                    print("You have logged out!")
                    break
                else:
                    print("Invalid Choice in Sub-Menu.")
    elif user_choice == "3":
        print("Thank you for using ATM.")
        break
    else:
        print("Invalid Choice in Main Menu.")

