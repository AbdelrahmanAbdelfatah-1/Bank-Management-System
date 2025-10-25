import time
import datetime
import json

try :
    file = open("Bank_Data.json", "r")
    Bank_Data = json.load(file)
    file.close()
except :
    Bank_Data = []

USD_value = 48.45
SAR_value = 12.91

while True :

    Main_flag = True
    print("\n############ Welcome to SIC Bank Management System ############\n")
    print("If you already have an account please enter login ")
    print("If you do not have an account please enter sign up ")
    print("Enter exit if you need to exit")

    x = (input("▶️ ").lower()).strip()

    if x == "login" :

        print( "############ ًWelcome to login page ############" )

        while True :

            try:
                ID = int(input("Enter your ID : "))
            except :
                print("Invalid ID. Please enter a number.")
                continue

            if not 0 <= ID < len(Bank_Data) :
                print("ID not found.")
                continue

            if not Bank_Data[ID]["Account_status"] :
                print("Your account has been closed and you will not be able to access it until You go to bank branch because you exceeded the allowed login attempts.")
                Main_flag = False
                break

            if Bank_Data[ID]["Lock_time"] :

                remaining_time = time.time() - Bank_Data[ID]["Lock_time"]

                if remaining_time < 30 :

                    print(f"your account is locked please try again after {int(30-remaining_time)} seconds.")
                    Main_flag = False
                    break

                else:

                    Bank_Data[ID]["Lock_time"] = None
                    Bank_Data[ID]["Temp_faild_tries"] = 0

                    file = open("Bank_Data.json", "w")
                    json.dump(Bank_Data, file, indent=4)
                    file.close()

            Password = input("Enter your password : ")

            if Bank_Data[ID]["Password"] == Password :

                print(f"############ Welcome {Bank_Data[ID]['Name']} ############")

                Bank_Data[ID]["Temp_faild_tries"] = 0
                Bank_Data[ID]["perm_faild_tries"] = 0

                file = open("Bank_Data.json", "w")
                json.dump(Bank_Data, file, indent=4)
                file.close()

                break

            else :

                print("Wrong password")

                Bank_Data[ID]["Temp_faild_tries"] += 1
                Bank_Data[ID]["perm_faild_tries"] += 1

                if Bank_Data[ID]["Temp_faild_tries"] >= 3 :
                    Bank_Data[ID]["Lock_time"] = time.time()

                if Bank_Data[ID]["perm_faild_tries"] >= 10 :

                    print("Your account has been closed and you will not be able to access it until You go to bank branch because you exceeded the allowed login attempts.")

                    Bank_Data[ID]["Account_status"] = False

                    file = open("Bank_Data.json", "w")
                    json.dump(Bank_Data, file, indent=4)
                    file.close()

                    Main_flag = False
                    break

                file = open("Bank_Data.json", "w")
                json.dump(Bank_Data, file, indent=4)
                file.close()

                continue

        if not Main_flag :
            continue

        while (True) :

            print("Please enter your choice : ")
            print("[0] Deposit")
            print("[1] Withdraw")
            print("[2] Transfer")
            print("[3] Check balance & Personal informations")
            print("[4] Exit")

            try :
                choice = int(input("\nEnter your choice number : "))
            except :
                print("Wrong data please try again")
                continue

            if choice == 0 :

                print("######## Deposit ########")

                while True :

                    flag = False

                    print("The currently available currencies are (USD,EGP,SAR)  ")
                    amount = input("Please enter the amount and currency (5 EGP) : ").strip().split()

                    if len(amount) == 2 :

                        num = float( amount[0] )
                        currency = amount[1].upper()

                        if currency == "USD":

                            value = USD_value * num
                            Bank_Data[ID]["Balance"] += value
                            flag = True

                        elif currency == "SAR":

                            value = SAR_value * num
                            Bank_Data[ID]["Balance"] += value
                            flag = True

                        elif currency == "EGP":
                            value = num
                            Bank_Data[ID]["Balance"] += value
                            flag = True

                        else:
                            print("Invalid currency, The currently available currencies are (USD,EGP,SAR)")
                            continue

                        if flag :

                            Bank_Data[ID]["Operations"].append(f"Depositing {value} EGP in {datetime.datetime.now()} " )

                            file = open("Bank_Data.json", "w")
                            json.dump(Bank_Data, file, indent=4)
                            file.close()

                            print("The deposit operation was completed successfully.")
                            print(f"Your balance is : {Bank_Data[ID]["Balance"]} Eygtion Pound")
                            break

                    else:

                        print("Invalid input format, Please use format (5 EGP)")
                        continue

            elif choice == 1 :

                print("######### Withdraw #########")

                while True :

                    flag = False

                    print("The currently available currencies are (USD,EGP,SAR)  ")
                    amount = input("Please enter the amount and currency (5 EGP) : ").strip().split()

                    if len(amount) == 2:

                        num = float ( amount[0] )
                        currency = amount[1].upper()

                        if currency == "USD"   :
                            egp_equivalent = num * USD_value
                            flag = True
                        elif currency == "SAR" :
                            egp_equivalent = num * SAR_value
                            flag = True
                        elif currency == "EGP" :
                            egp_equivalent = num
                            flag = True
                        else:
                            print("Invalid currency, The currently available currencies are (USD,EGP,SAR)")
                            continue

                        if flag :

                            if Bank_Data[ID]['Balance'] >= egp_equivalent :

                                Bank_Data[ID]["Operations"].append(f"Withdrawing {egp_equivalent} EGP in {datetime.datetime.now()} ")
                                Bank_Data[ID]['Balance'] -= egp_equivalent

                                file = open("Bank_Data.json", "w")
                                json.dump(Bank_Data, file, indent=4)
                                file.close()

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

            elif choice == 2 :

                print("######### Transfer #########")

                while True :

                    try :
                        recipient_id = int(input("Enter recipient's ID: "))
                        break

                    except :
                        print("Invalid ID. Please enter a number.")
                        continue

                if 0 <= recipient_id < len ( Bank_Data ) and recipient_id != ID :

                    print(f"Transfer to: {Bank_Data[recipient_id]['Name']}")

                    while True :

                        flag = False
                        print("The currently available currencies are (USD,EGP,SAR)")
                        amount = input("Please enter the amount and currency (5 EGP) : ").strip().split()

                        if len(amount) == 2 :

                            num = float(amount[0])
                            currency = amount[1].upper()

                            if currency == "USD"   :
                                egp_equivalent = num * USD_value
                                flag = True
                            elif currency == "SAR" :
                                egp_equivalent = num * SAR_value
                                flag = True
                            elif currency == "EGP" :
                                egp_equivalent = num
                                flag = True

                            else:
                                print("Invalid currency, The currently available currencies are (USD,EGP,SAR)")
                                continue

                            if flag :

                                if Bank_Data[ID]["Balance"] >= egp_equivalent:

                                    Bank_Data[ID]["Balance"] -= egp_equivalent
                                    Bank_Data[ID]["Operations"].append(f"Transferring {egp_equivalent} EGP in {datetime.datetime.now()} to {Bank_Data[recipient_id]['Name']} with ID : {recipient_id}")
                                    Bank_Data[recipient_id]["Operations"].append(f"Receiving {egp_equivalent} EGP in {datetime.datetime.now()} from {Bank_Data[ID]['Name']} with ID : {ID}")
                                    Bank_Data[recipient_id]["Balance"] += egp_equivalent

                                    file = open("Bank_Data.json", "w")
                                    json.dump(Bank_Data, file, indent=4)
                                    file.close()

                                    print("The transfer operation was completed successfully.")
                                    print(f"Your balance is : {Bank_Data[ID]['Balance']} Egyptian Pound")
                                    break

                                else :

                                    print("Insufficient balance!")
                                    print(f"Your current balance is : {Bank_Data[ID]['Balance']} Egyptian Pound")
                                    break

                        else :

                            print("Invalid input format, Please use format (5 EGP)")
                            continue

                else :

                    print("Recipient ID not found!")

            elif choice == 3 :

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

            elif choice == 4 :

                v = int(input("Please rate our services from 1 to 10 where 1 is the worst and 10 is the best : ").strip())

                if 10 >= v > 5 :
                    print("Thanks for Rating ")
                else:
                    note = input("What are the problems you faced so we can solve them next time ? \n ▶️ ")
                    print("Alright, we will take this into consideration.")

                break

            else :

                print ("please enter number from 0 to 4")
                continue

            cont = input("Do you want The services list again ? (yes/no) : ").lower().strip()

            if cont == "no":

                v = int( input("Please rate our services from 1 to 10 where 1 is the worst and 10 is the best : ").strip())

                if 10 >= v > 5 :
                    print("Thanks for Rating ")
                else:
                    note = input("What are the problems you faced so we can solve them next time ? \n ▶️ ")
                    print("Alright, we will take this into consideration.")

                break

    elif x == "sign up" :

        print("############ Welcome to sign up page ############")

        Name = input("Enter your Name : ")
        ID = len(Bank_Data)
        Password = input("Enter your password : ")
        confirm_password = input("Confirm your password : ")
        if Password != confirm_password:
            print("Passwords do not match ")
            continue
        PhoneNumber = input("Enter your Phone Number : ")
        Email = input("Enter your Email Address : ")
        Gender = input("Enter your Gender : ")
        Age = input("Enter your Age : ")
        City = input("Enter your City : ")

        User_Data = {
            "Name": Name ,
            "ID": ID     ,
            "Password": Password      ,
            "PhoneNumber": PhoneNumber,
            "Email": Email    ,
            "Gender": Gender  ,
            "Age": Age     ,
            "City": City   ,
            "Balance":  0  ,
            "Operations": [] ,
            "Account_status": True,
            "Temp_faild_tries": 0,
            "perm_faild_tries": 0,
            "Lock_time": None
        }

        Bank_Data.append(User_Data)

        file = open("Bank_Data.json", "w")
        json.dump(Bank_Data, file, indent=4)
        file.close()

        print(f"Sign in successful, Your ID is {ID}")
        print("You will Go to the main page to login and use our services ")
        print()

    elif x == "exit" :
        print("############ Goodbye I wish you a happy day ############")
        break

    else:
        print("Wrong data please try again")


