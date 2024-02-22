# =============================================================================
# Decrypting (OPTIONAL) (Start of CTRL + / here)
# =============================================================================

def decrypt_zip(encrypted_zip_path, password, output_folder):
    # Make sure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Open the encrypted zip file
    with pyzipper.AESZipFile(encrypted_zip_path) as zf:
        # Set the password for decryption
        zf.setpassword(password.encode('utf-8'))

        # Extract all the contents to the output folder
        zf.extractall(output_folder)
        print(f"Extracted {encrypted_zip_path} to {output_folder}")


# Set the password to the known decryption password
password = 'Xavier'

# Specify the root directory where the encrypted zip files are located
root_folder = os.getcwd()
client_encrypt_folder = os.path.join(root_folder, 'clientClean')

# Specify the output directory for decrypted files
client_decrypt_folder = os.path.join(root_folder, 'clientDecrypt')

# Loop over all zip files in the encrypted folder
for zip_filename in os.listdir(client_encrypt_folder):
    if zip_filename.endswith('.zip'):
        # Get the full path to the encrypted zip file
        encrypted_zip_path = os.path.join(client_encrypt_folder, zip_filename)
        # Call the decrypt function
        decrypt_zip(encrypted_zip_path, password, client_decrypt_folder)

# =============================================================================
# End of Section (OPTIONAL) (End of CTRL + / here)
# =============================================================================
