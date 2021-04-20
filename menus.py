import os
import io
import sys

import GDrive
import admin
import main
#import encrypt

# Function to print options available to Admin
def print_admin_options():
    print('[ADD] Type `ADD` to add a new user to group')
    print('[DEL] Type `DEL` to delete a user from the group')
    print('[MENU] Type `MENU` to go to the files menu')
    print('[EXIT] Type `EXIT` to exit')

# Function to give admin-menu to admin and take input
    # 4 options - ADD, Remove, Menu, Exit
def get_admin_menu():
    exit = False
    while exit == False:
        try:
            print("--- Admin Menu ---")
            
            # Print the list of options available to Admin
            print_admin_options()
            
            # Take Input and check what the admin wants to do
                # If Input is not recognised, give the options again
            user_input = input("\n>> ")

            if str.upper(user_input) == "ADD":
                admin.sign_up()
            
            elif str.upper(user_input) == "DEL":
                admin.remover_User()
            
            elif str.upper(user_input) == "MENU":
                get_regular_menu()
            
            elif str.upper(user_input) == "EXIT":
                exit = True
            
            else: 
                print("Input not recognised. Please select an option again")     
                get_admin_menu()

        except KeyboardInterrupt:
            admin.exit()    
    
    admin.exit()


# Function to print options available to the group
    # If admin is signed-in, an extra feature given to go to the Admin's Menu
def print_regular_menu_options():
    print('[UPLOAD] Type `UPLOAD` to encrypt a file and upload it on Google Drive')
    print('[DOWNLOAD] Type `DOWNLOAD` to download a file and decrypt it')
    
    if main.is_current_user_admin == True:
        print('[ADMIN] Type `ADMIN` to access Admin Menu')
    
    print('[EXIT] Type `EXIT` to exit')
    #print('[MENU] Type `MENU` to go to the files menu')
    


# # Function to give menu to goup member and take input
    # 3 options - UPLOAD, DOWNLOAD, Exit
    # If user is admin, 1 option more - Go to ADMIN menu
def get_regular_menu():
    exit = False
    while exit == False:
        try:
            print("--- Menu ---")
            
            # Print the list of options available to Admin
            print_regular_menu_options()
            
            # Take Input and check what the admin wants to do
                # If Input is not recognised, give the options again
            user_input = input("\n>> ")

            if str.upper(user_input) == "UPLOAD":
                print("upload_function() called")
            
            elif str.upper(user_input) == "DOWNLOAD":
                print("download_function() called")
            
            elif str.upper(user_input) == "ADMIN" and main.is_current_user_admin == True:
                get_admin_menu()

            elif str.upper(user_input) == "EXIT":
                exit = True
            
            else: 
                print("Input not recognised. Please select an option again")     
                get_regular_menu()

        except KeyboardInterrupt:
            admin.exit()    
    
    admin.exit()
