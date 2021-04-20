import os
import io
import sys
import GDrive
import admin

# Global Variable used to check if signed-in user is Admin or Not
is_current_user_admin = False

def main():

    
    admin.sign_in()
    # print("Type Download to Download Files from Google Drive.")

    # loop_end = 0
    # while(loop_end != 1):
    #     user_response = input()
    #     if user_response == 'Download':
    #         GDrive.download_file()
    #     else :
    #         print("Trouble getting input. Please Try Again")    


if __name__ == '__main__':
    print("\n\nWELCOME TO TANMAY's SECURE CLOUD APP")
    main()
