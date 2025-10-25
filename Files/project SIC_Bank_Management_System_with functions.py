import json, time, datetime
file_name = "Bank_Data.json"
USD_value = 48.45
SAR_value = 12.91

def read_data_from_json() :
    try :
        with open(file_name, "r") as file :
            return json.load(file)
    except :
        return []
def write_data_from_json(data) :
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)
def convert_to_egp(amount, currency):
    if currency == "USD":
        return amount * USD_value
    elif currency == "SAR":
        return amount * SAR_value
    elif currency == "EGP":
        return amount
    else:
        return False
def rate_services():
    v = int(input("Please rate our services from 1 to 10: ").strip())
    if 10 >= v > 5:
        print("Thanks for Rating")
    else:
        note = input("What are the problems you faced so we can solve them next time?\n▶️ ")
        print("Alright, we will take this into consideration.")
def chek_password_sign_up():
    password = input("Enter your password : ")
    confirm_password = input("Confirm your password : ")
    if password != confirm_password :
        print("Passwords do not match ")
        return None
    return password
def sign_up():
    print("############ Welcome to sign up page ############")

    Name = input("Enter your Name : ")
    ID = len(Bank_Data)
    Password = chek_password_sign_up()
    if not Password :
        return False
    PhoneNumber = input("Enter your Phone Number : ")
    Email = input("Enter your Email Address : ")
    Gender = input("Enter your Gender : ")
    Age = input("Enter your Age : ")
    City = input("Enter your City : ")

    User_Data = {
        "Name": Name,
        "ID": ID,
        "Password": Password,
        "PhoneNumber": PhoneNumber,
        "Email": Email,
        "Gender": Gender,
        "Age": Age,
        "City": City,
        "Balance": 0,
        "Operations": [],
        "Account_status": True,
        "Temp_faild_tries": 0,
        "perm_faild_tries": 0,
        "Lock_time": None
    }
    return User_Data
def Program_interface () :
    print("\n############ Welcome to SIC Bank Management System ############\n")
    print("If you already have an account please enter login ")
    print("If you do not have an account please enter sign up ")
    print("Enter exit if you need to exit")
def show_menu ():
    print("Please enter your choice : ")
    print("[0] Deposit")
    print("[1] Withdraw")
    print("[2] Transfer")
    print("[3] Check balance & Personal informations")
    print("[4] Exit")
def deposit ():

    print("######## Deposit ########")

    while True:

        print("The currently available currencies are (USD,EGP,SAR)  ")
        amount = input("Please enter the amount and currency (5 EGP) : ").strip().split()

        if len(amount) == 2:

            num = float(amount[0])
            currency = amount[1].upper()
            value = convert_to_egp(num,currency)
            if value == False :
                print("Invalid currency, The currently available currencies are (USD,EGP,SAR)")
                continue
            else :
                Bank_Data[ID]["Balance"] += value

            Bank_Data[ID]["Operations"].append(f"Depositing {value} EGP in {datetime.datetime.now()} ")

            write_data_from_json(Bank_Data)

            print("The deposit operation was completed successfully.")
            print(f"Your balance is : {Bank_Data[ID]["Balance"]} Eygtion Pound")
            break

        else:
            print("Invalid input format, Please use format (5 EGP)")
            continue
def withdraw():
    print("######### Withdraw #########")

    while True:

        print("The currently available currencies are (USD,EGP,SAR)  ")
        amount = input("Please enter the amount and currency (5 EGP) : ").strip().split()

        if len(amount) == 2:

            num = float(amount[0])
            currency = amount[1].upper()
            value = convert_to_egp(num,currency)
            if value == False :
                print("Invalid currency, The currently available currencies are (USD,EGP,SAR)")
                continue
            else :
                egp_equivalent = value

            if Bank_Data[ID]['Balance'] >= egp_equivalent:

                Bank_Data[ID]["Operations"].append(f"Withdrawing {egp_equivalent} EGP in {datetime.datetime.now()} ")
                Bank_Data[ID]['Balance'] -= egp_equivalent

                write_data_from_json(Bank_Data)

                print("The withdraw operation was completed successfully.")
                print(f"Your balance is : {Bank_Data[ID]['Balance']} Egyptian Pound")

                break

            else:

                print("Insufficient balance!")
                print(f"Your current balance is : {Bank_Data[ID]['Balance']} Egyptian Pound")
                break

        else:
            print("Invalid input format, Please use format (5 EGP)")
            continue
def transfer():
    print("######### Transfer #########")

    while True:

        recipient_id = check_recipient_ID()
        if recipient_id == None :
            continue

        print("The currently available currencies are (USD,EGP,SAR)")
        amount = input("Please enter the amount and currency (5 EGP) : ").strip().split()

        if len(amount) == 2:

            num = float(amount[0])
            currency = amount[1].upper()
            value = convert_to_egp(num, currency)
            if value == False:
                print("Invalid currency, The currently available currencies are (USD,EGP,SAR)")
                continue
            else:
                egp_equivalent = value

            if Bank_Data[ID]["Balance"] >= egp_equivalent:

                Bank_Data[ID]["Balance"] -= egp_equivalent
                Bank_Data[ID]["Operations"].append(f"Transferring {egp_equivalent} EGP in {datetime.datetime.now()} to {Bank_Data[recipient_id]['Name']} with ID : {recipient_id}")
                Bank_Data[recipient_id]["Operations"].append(f"Receiving {egp_equivalent} EGP in {datetime.datetime.now()} from {Bank_Data[ID]['Name']} with ID : {ID}")
                Bank_Data[recipient_id]["Balance"] += egp_equivalent

                write_data_from_json(Bank_Data)

                print("The transfer operation was completed successfully.")
                print(f"Your balance is : {Bank_Data[ID]['Balance']} Egyptian Pound")
                break

            else:

                print("Insufficient balance!")
                print(f"Your current balance is : {Bank_Data[ID]['Balance']} Egyptian Pound")
                break

        else:

            print("Invalid input format, Please use format (5 EGP)")
            continue
def personal_informations ():
    print("##### Check balance & Personal informations #####")
    print(f"Name : {Bank_Data[ID]['Name']}")
    print(f"ID : {Bank_Data[ID]['ID']}")
    print(f"Email : {Bank_Data[ID]['Email']}")
    print(f"Phone : {Bank_Data[ID]['PhoneNumber']}")
    print(f"Gender : {Bank_Data[ID]['Gender']}")
    print(f"Age : {Bank_Data[ID]['Age']}")
    print(f"City : {Bank_Data[ID]['City']}")
    print(f"Balance : {Bank_Data[ID]['Balance']} Egyptian Pound")
    print("The operations did you have : ")
    for operation in Bank_Data[ID]['Operations']:
        print(operation)
def check_ID ():
    try :
        ID = int(input("Enter your ID: "))
        _ = Bank_Data[ID]
        return ID
    except ValueError :
        print("Invalid ID. Please enter a number.")
        return None
    except IndexError :
        print("ID not found!")
        return None
def check_recipient_ID ():
    try :
        recipient_id = int(input("Enter the recipient ID: "))
        _ = Bank_Data[recipient_id]
        return recipient_id
    except ValueError :
        print("Invalid ID. Please enter a number.")
        return None
    except IndexError :
        print("ID not found!")
        return None
def check_password_Login():
    Password = input("Enter your password : ")

    if Bank_Data[ID]["Password"] == Password :

        print(f"############ Welcome {Bank_Data[ID]['Name']} ############")

        Bank_Data[ID]["Temp_faild_tries"] = 0
        Bank_Data[ID]["perm_faild_tries"] = 0

        write_data_from_json(Bank_Data)

        return 0

    else:

        print("Wrong password")

        Bank_Data[ID]["Temp_faild_tries"] += 1
        Bank_Data[ID]["perm_faild_tries"] += 1

        if Bank_Data[ID]["Temp_faild_tries"] >= 3:
            Bank_Data[ID]["Lock_time"] = time.time()

        if Bank_Data[ID]["perm_faild_tries"] >= 10:
            print("Your account has been closed and you will not be able to access it until You go to bank branch because you exceeded the allowed login attempts.")

            Bank_Data[ID]["Account_status"] = False

            write_data_from_json(Bank_Data)

            return -1

        write_data_from_json(Bank_Data)
        return 1
def lock_time_30sec ():
    if Bank_Data[ID]["Lock_time"]:

        remaining_time = time.time() - Bank_Data[ID]["Lock_time"]

        if remaining_time < 30:

            print(f"your account is locked please try again after {int(30 - remaining_time)} seconds.")
            return False

        else:

            Bank_Data[ID]["Lock_time"] = None
            Bank_Data[ID]["Temp_faild_tries"] = 0

            write_data_from_json(Bank_Data)
    return True
def lock_time_perm ():
    if not Bank_Data[ID]["Account_status"]:
        print("Your account has been closed and you will not be able to access it until You go to bank branch because you exceeded the allowed login attempts.")
        return True
    return False

while True :

    Main_flag = True
    Bank_Data = read_data_from_json()
    Program_interface()

    x = (input("▶️ ").lower()).strip()

    if x == "login" :

        print( "############ ًWelcome to login page ############" )

        while True :

            ID = check_ID()

            if ID == None :
                continue

            lock_perm = lock_time_perm()

            if lock_perm == True :
                Main_flag = False
                break

            Lock = lock_time_30sec()

            if Lock == False :
                Main_flag = False
                break

            Pass = check_password_Login()

            if Pass == 0 :
                break
            elif Pass == 1 :
                continue
            else :
                Main_flag = False
                break

        if not Main_flag :
            continue

        while (True) :

            show_menu()

            try :
                choice = int(input("\nEnter your choice number : "))
            except :
                print("Wrong data please try again")
                continue

            if choice == 0 :
                deposit()
            elif choice == 1 :
                withdraw()
            elif choice == 2 :
                transfer()
            elif choice == 3 :
                personal_informations()
            elif choice == 4 :
                rate_services()
                break
            else :
                print ("please enter number from 0 to 4")
                continue

            cont = input("Do you want The services list again ? (yes/no) : ").lower().strip()

            if cont == "no":
                rate_services()
                break

    elif x == "sign up" :

        User_Data = sign_up()
        if User_Data == False :
            continue
        Bank_Data.append(User_Data)
        write_data_from_json(Bank_Data)

        print(f"Sign in successful, Your ID is {User_Data['ID']}")
        print("You will Go to the main page to login and use our services ")
        print()

    elif x == "exit" :
        print("############ Goodbye I wish you a happy day ############")
        break

    else :
        print("Wrong data please try again")



