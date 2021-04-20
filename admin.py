import os
import io
import sys
import getpass
import pickle
import menus
menu = menus

# Function to write data in a file
def writeToFile(obj, filename):
	with open(filename, 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# Function to read data from the file
    # Stores Usernames and Passwords in a file called accounts.pkl
def readFromFile(filename):
	if os.path.getsize("accounts.pkl") > 0:
		with open(filename, 'rb') as f:
			return pickle.load(f)
	else:
		return {}

# Loads all the usernames and passwords into accounts
accounts = readFromFile("accounts.pkl")

# Function to get user credentials to Sign-In
    # If there are no users, prompt the user to create a new user
    # If there are users, prompt the user for their username and password
def sign_in():
    try:
        
        # If no users in the application file, create a new user
        if os.path.getsize("accounts.pkl") == 0:
            sign_up()

        # Get Username and Password for Authentication
        username, password = get_credentials()   
        

        # If credentials match, show menu
            # If username is admin 
            # If a regular group member, show regular menu
        if username in accounts and accounts[username] == password :
            if username == "admin" :
                print("Welcome, Admin! Sign-In Successful")                         
                menu.get_admin_menu()
            else:
                print("Sign-In Successful")
                menu.get_regular_menu()
        
        # Credentials do not match. Ask if you want to try again.
        else:
            print("Sign-In Unsuccessful. Do you want to try again? (Yes or No)")
            response = input()
            if response == "Yes":
                sign_in()    
            else :
                exit()    

    except KeyboardInterrupt:
        exit()    

# Function to retreive username and password from the user input
def get_credentials():
    print("Please enter your CREDENTIALS to sign in\n\n")
    
    try :
        # Ask for Username
        username = input("Username : ")
        
        # Get Pass method to get password
        password = getpass.getpass()

        return username, password
    except KeyboardInterrupt:
        exit()    

    
# Function to sign-up a new user
def sign_up():
    print("Please choose an Username & Password to Sign-Up\n\n")
    
    try :
        print("--- SIGN-UP ---")
        # Ask for Username
        username = input("Username : ")
        
        duplicate_username = True
        # Check for no duplicate username
        while duplicate_username == True:
            if username in accounts :
                print("This username has been taken. Please Choose a new one.")
                # Ask for Username
                username = input("Username : ")
            else :
                duplicate_username = False
                
                # Get Pass method to get password
                password = getpass.getpass()
                
                # Store the username and password in accounts
                accounts[username] = password     
                writeToFile(accounts,"accounts.pkl")
                print("Sign-Uo Successful.")

                # Navigate to Admin's Menu as only admin can sign new people up
                menu.get_admin_menu()
  
    except KeyboardInterrupt:
        exit() 

def remover_User():
    print("Please enter the username of the person to remove the user from the group")
    try :
        # Ask for Username
        username = input("Username : ")
        
        # Check if Username is in accounts
        if username in accounts:
            del accounts[username]
            writeToFile(accounts,"accounts.pkl")
            print(username," Removed" )

        else:
            print(username," does not exist")
 
    except KeyboardInterrupt:
        exit()

# Function to close the application
def exit():
    print("\n-->  TK Secure Cloud App Shutting Down...\nGoodbye.")
    sys.exit()

