import io
import os
import rsa
from cryptography.fernet import Fernet

# This program is used to produce Public and Private Keys. 
# Key.key (which is used by AES algorithm) file is the text we want to encrypt using Public and Private Keys.
# Reason - AES is the key which can decrypt any file on the Google Drive
# Solution - We use RSA protocol to share key.key file using Public and Private Keys


# key.key = Plain Text

# Function to Generate Public and Private Keys
    # Takes Username and Creates a folder in the User's Section with that name
    # Generates Public and Private Keys for that user
    # Stores the User's Public and Private Keys in the user's folder
def generate_RSA_keys(username):
    try:
        # Create a Folder in the Users folder with the name of the new User
        directory = username
        parent_dir = "Users/"
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)

        # Generate Public Key and Private Key for the user
        (public_key, private_key) = rsa.newkeys(2048)

        # Write Public Key in file called public.key
        pub_path = path+"/public.key"
        public_file = open(pub_path, 'wb')
        public_file.write(public_key.save_pkcs1('PEM'))
        public_file.close()

        # Write Private Key in file called private.key
        priv_path = path+"/private.key"
        private_file = open(priv_path, 'wb')
        private_file.write(private_key.save_pkcs1('PEM'))
        private_file.close()

        status = True
        return status

    except:
        status = False
        return status

# Function to encrypt AES key using Public Key of the selected User
def rsa_encrypt(username):
    try:
        # Get Data from the key.key (AES Key) which is Plain Text
        aes_key = open('key.key', 'rb')
        key_data = aes_key.read()

        # Encrypt the key.key file using Public Key of the user
        # Get the key from the public key file
        path = 'Users/'+username
        temp_path = path +'/public.key'
        pub_key = open(temp_path,'r')
        pub_key_data = pub_key.read()

        # Load the Data from the file
        public_key = rsa.PublicKey.load_pkcs1(pub_key_data)

        # Encrypt the AES key
        encrypted_aes_key = rsa.encrypt(key_data, public_key)
        
        # Create a file called AES_encrypted
        new_path = path+'/AES_encrypted'
        file = open(new_path,'wb')
        file.write(encrypted_aes_key)
        print("AES key successfully encrypted using Public Key")
        print("Your encrypted AES key is this : \n\n",encrypted_aes_key)
    except KeyboardInterrupt():
        print("AES key could not be encrypted using the Public Key")    

def rsa_decrypt(username):
    
    # Get the Private Key file
    path = 'Users/'+username
    temp_path = path +'/private.key'
    priv_key = open(temp_path,'rb')
    private_key_data = priv_key.read()

    # Get Private Key
    private_key = rsa.PrivateKey.load_pkcs1(private_key_data)
    
    # Get Encrypted AES File
    new_path = path+'/AES_encrypted'
    e = open(new_path,'rb')
    aes_enc = e.read()

    decrypted_key = rsa.decrypt(aes_enc, private_key)
    
    print("\n\nAES Key after RSA and Decryption Encryption  = ", decrypted_key)
    print("\n\n")

    

def main():
    username = input("You can test RSA encryption by running this file. Type a name of any user from the User's Folder.\n>>")
    # Check Encryption
        # See if a new file by the name of AES_encrypted is created in the User's Folder
    # Encrypt and Decrypt
    rsa_encrypt(username)
    rsa_decrypt(username)
    
    # Orignal AES Key
    aes_key = open('key.key', 'rb')
    key_data = aes_key.read()
    print("\nORIGNAL AES Key = ",key_data)


if __name__ == '__main__':
    main()        