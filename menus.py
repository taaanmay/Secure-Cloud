import os
import io
import sys

import GDrive
import admin
import main
import encrypt
import rsa_encryption

googleDrive = GDrive
encryption = encrypt

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
	print('[LIST] Type `LIST` to list the files on Drive')
	if main.is_current_user_admin == True:
		print('[ADMIN] Type `ADMIN` to access Admin Menu')
	print('[EXIT] Type `EXIT` to exit')
	#print('[MENU] Type `MENU` to go to the files menu')
	


# # Function to give menu to goup member and take input
	# 3 options - UPLOAD, DOWNLOAD, LIST, EXIT
	# If user is admin, 1 option more - Go to ADMIN menu
def get_regular_menu():
	exit = False
	while exit == False:
		try:
			print("\n--- Menu ---")
			
			# Print the list of options available to Admin
			print_regular_menu_options()
			
			# Take Input and check what the admin wants to do
				# If Input is not recognised, give the options again
			user_input = input("\n>> ")

			if str.upper(user_input) == "UPLOAD":
				filename = input("\nEnter the filename you want to upload : ")
				path = "Uploads/" + filename
				
				if os.path.exists(path):
					# Encrypt the file
					encrypted_file_name = encryption.encrypt_file(encryption.get_key(), filename)

					# If file was encrypted upload the file
					if encrypted_file_name != None:
						# Update Path to the Encrypted File
						#new_path = "Uploads/" + encrypted_file_name
						new_path = encrypted_file_name
						# Upload File
						googleDrive.upload_file(encrypted_file_name, new_path)

						# Remove encrypted file
						os.remove(encrypted_file_name)

					# If file was not encrypted, ask the user if wants to upload the file without Encryption
					else:
						resp = input("File could not be encripted. Do you want to upload the file without encryption? (Yes/No)")
						if str.upper(resp) == "YES":
							googleDrive.upload_file(filename, path)	
						else:
							print("File not uploaded.")	
							

				else:
					print("PATH >> ",path)
					print("File could not be found. Please check if the file is in Uploads Folder")	
			
			elif str.upper(user_input) == "DOWNLOAD":
				
				filename = input("\nEnter the filename you want to download : ")
				# Get File ID 
				file_ID = googleDrive.get_file_id("name contains '"+filename+"'")

				if file_ID != -1 :
					# Download File from the drive
					googleDrive.download_file(file_ID, filename)

					# Decrypt the File and Store in Download Folder
					down_file = encryption.decrypt_file(filename)
					print(down_file," has been decrypted and stored in the Downloads folder")

					# Delete the downloaded encrypted file
					os.remove("Downloads/"+filename)
				else:
					print("File Not Found on Drive.")

			elif str.upper(user_input) == "LIST":
				googleDrive.list_files()
			
			
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
