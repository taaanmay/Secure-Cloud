import os
import io
import sys
import GDrive
import admin


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