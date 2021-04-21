import os
import io
import sys


from Crypto import Random
import struct

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Generate Key using Crypto.Random method and write in key.key file
def generate_key():
	key = get_random_bytes(16)
	
	# Store key in key.key file
	file = open('key.key', 'wb')
	file.write(key)
	file.close()

# Retreive key from key.key file
def get_key():
	if os.path.getsize('key.key') != 0:
		file = open('key.key', 'rb')
		key = file.read()
		file.close()
		return key
	else:
		generate_key()
		return get_key()


# Encrypt file using key and return the encrypted file name
def encrypt_file(key, filename):
	path = "Uploads/"+filename
	
	#encrypted_file_name = filename + '.enc'
	encrypted_file_name = '(enc)'+filename 
	#encrypted_file_path = 'Uploads/'+encrypted_file_name
	
	filesize = str(os.path.getsize(path)).zfill(16)
	chunk_size = 64*1024

	# Intialisation Vector = 16 random bytes
	iv = Random.new().read(16)
	
	encryptor = AES.new(key, AES.MODE_CBC, iv)

	with open(path,'rb') as infile:
		with open(encrypted_file_name, 'wb') as outfile:
			outfile.write(filesize.encode('utf-8'))
			outfile.write(iv)
			
			while True:
				chunk = infile.read(chunk_size)
				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += b' ' * (16 - (len(chunk) % 16))
				
				outfile.write(encryptor.encrypt(chunk))
	
	return encrypted_file_name



	
def decrypt_file(filename):
	key = get_key()
	path = "Downloads/" + filename
	
	print("Decrypting ", filename)

	chunk_size = 64*1024
	
	# Removing (enc) from  the filename 
	decrypted_file_name = filename[5:]
	
	# Decryption
		# Open Encrypted File
	with open(path, 'rb') as infile:
		filesize = int(infile.read(16))
		iv = infile.read(16)
		decryptor = AES.new(key, AES.MODE_CBC, iv)
		
		with open("Downloads/"+decrypted_file_name, 'wb') as outfile:
			while True:
				chunk = infile.read(chunk_size)
				if len(chunk) == 0:
					break
				outfile.write(decryptor.decrypt(chunk))
			
			outfile.truncate(filesize)
	
	return decrypted_file_name		
