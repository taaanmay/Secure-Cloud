import os
import io
import sys
import GDrive
import admin

# Global Variable used to check if signed-in user is Admin or Not
is_current_user_admin = False

def main():
    admin.sign_in()
        


if __name__ == '__main__':
    print("\n\nWELCOME TO TANMAY's SECURE CLOUD APP")
    main()
