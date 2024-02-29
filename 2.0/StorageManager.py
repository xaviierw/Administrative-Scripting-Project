import os
import pyftpdlib
import shutil
import logging
import datetime
import zipfile
import re
import time
import pyzipper
from pyzipper import AESZipFile
from datetime import date
from datetime import datetime
from ftplib import FTP
from cryptography.fernet import Fernet
from zipfile import ZipFile, ZIP_DEFLATED
from ftplib import FTP, error_perm
from time import sleep

# =============================================================================
# Section A Part 1 - Connecting to FTP (Start of CTRL + / here)
# =============================================================================

# =============================================================================
# SETUP: Logging Configuration
# =============================================================================

log_file_path = os.path.join(os.getcwd(), 'summary.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
# =============================================================================
# SECTION: Function Definition & Create Local Directory
# =============================================================================
def server_folder(ftp, folder, local_dir):
    try:
        os.makedirs(local_dir, exist_ok=True)
    except OSError as e:
        logging.error(f"Error creating local directory {local_dir}: {e}")
        return

# =============================================================================
# SECTION: Change to FTP Directory (Change Working Directory)
# =============================================================================
    try:
        ftp.cwd(folder)
    except Exception as e:
        logging.error(f"Error changing to FTP directory {folder}: {e}")
        return

# =============================================================================
# SECTION: List Items in FTP Directory
# =============================================================================

    items = ftp.nlst()

# =============================================================================
# SECTION: Process Items and Download
# =============================================================================

    for item in items:
        local_path = os.path.join(local_dir, item)
        try:
            if '.' in item:  # Assuming it's a file based on the presence of a dot
                # Attempt to get the file's modification time from the server
                resp = ftp.sendcmd('MDTM ' + item)
                # Parse the modification time from the response
                mtime = datetime.strptime(resp[4:], "%Y%m%d%H%M%S")
                # Convert to timestamp
                mtime_ts = mtime.timestamp()

                with open(local_path, 'wb') as local_file:
                    ftp.retrbinary('RETR ' + item, local_file.write)

                # Set the modification time of the local file to match the server's
                os.utime(local_path, (mtime_ts, mtime_ts))

                logging.info(f"Downloaded {item} to {local_path}")
            else:
                server_folder(ftp, item, local_path)
        except Exception as e:
            logging.error(f"Error downloading {item}: {e}")


def write_summary_file():
    current_time = datetime.now().strftime('%d/%m/%y %H:%M:%S')
    logging.info(f"Downloading files from FTP server completed at {current_time}.")

# =============================================================================
# SETUP: FTP Connection Parameters
# =============================================================================

ftp_host = '127.0.0.1'
ftp_user = 'admin'
ftp_passwd = 'admin'
ftp_folder = '/resource/do_not_touch' # FTP server path to the target folder
local_dir = os.path.join(os.getcwd(), 'history_a') # Local directory to store the downloaded contents

try:
    with FTP() as ftp:
        ftp.connect(host=ftp_host, port=22)
        ftp.login(ftp_user, ftp_passwd)
        logging.info("Connected and logged in to FTP server.")
        server_folder(ftp, ftp_folder, local_dir) # Begin downloading files
        write_summary_file()
except Exception as e:
    logging.error(f"Error connecting to or operating on the FTP server: {e}")

# =============================================================================
# End of Section A Part 1 (End of CTRL + / here)
#=============================================================================

# =============================================================================
# Section A Part 2 - Sorting files based on extensions (Start of CTRL + / here)
#  SETUP: Logging configuration
# =============================================================================

log_file_path = os.path.join(os.getcwd(), 'summary.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
def sort_files(source_dir, dest_img_dir, dest_txt_dir):
    os.makedirs(dest_img_dir, exist_ok=True)
    os.makedirs(dest_txt_dir, exist_ok=True)

    img_extensions = ['.img', '.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi', '.png', '.gif', '.bmp', '.dib', '.tiff',
                      '.tif', '.tga', '.heif', '.heic', '.webp']
    img_count = 0
    txt_count = 0

    for filename in os.listdir(source_dir):
        src_file_path = os.path.join(source_dir, filename)
        if os.path.isfile(src_file_path):
            _, file_extension = os.path.splitext(filename)
            if file_extension.lower() in img_extensions:
                dest_file_path = os.path.join(dest_img_dir, filename)
                shutil.move(src_file_path, dest_file_path)
                img_count += 1
            elif file_extension.lower() == '.txt':
                dest_file_path = os.path.join(dest_txt_dir, filename)
                shutil.move(src_file_path, dest_file_path)
                txt_count += 1

    logging.info("File sorting done.")

source_dir = os.path.join(os.getcwd(), 'history_a')
dest_img_dir = os.path.join(os.getcwd(), 'clientImage')
dest_txt_dir = os.path.join(os.getcwd(), 'clientText')

sort_files(source_dir, dest_img_dir, dest_txt_dir)

# =============================================================================
# End of Section A Part 2 (End of CTRL + / here)
# =============================================================================

# =============================================================================
# Section B - Detect anomalies  (Start of CTRL + / here)
#   SETUP: Logging configuration
# =============================================================================

log_file_path = os.path.join(os.getcwd(), 'summary.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def identify_virus_patterns(folder):
    virus_pattern = re.compile(r'\b[A-Za-z]{2}\d{6}\b')
    virus_files = []

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r') as file:
                content = file.read()
                matches = virus_pattern.findall(content)
                if matches:
                    # Log the file and the virus code identified
                    logging.info(f"Virus identified in file: {filename} with code(s): {', '.join(matches)}")
                    virus_files.append((filename, matches))

    logging.info("Scan for virus done.")

    return virus_files
folder = os.path.join(os.getcwd(), 'clientText')
virus_folder = os.path.join(os.getcwd(), 'virus')
os.makedirs(virus_folder, exist_ok=True)

virus_files = identify_virus_patterns(folder)

for file, _ in virus_files:
    src = os.path.join(folder, file)
    dst = os.path.join(virus_folder, file)
    shutil.move(src, dst)

# =============================================================================
# End of Section B (End of CTRL + / here)
# =============================================================================

# =============================================================================
# Section C - Encrypting and zipping of files (Start of CTRL + / here)
#  SETUP: Logging configuration
# =============================================================================

import datetime

log_file_path = os.path.join(os.getcwd(), 'summary.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(message)s')

def log_to_summary(file_path, archive_name):
    year = archive_name[:4]
    month = archive_name[4:6]
    month_name = datetime.datetime.strptime(month, "%m").strftime("%b")
    log_message = f"{file_path} created on {month_name} {year} archive to {archive_name}.zip"
    logging.info(log_message)

def create_encrypted_zip(files, archive_name, password, output_folder):
    zip_path = os.path.join(output_folder, f'{archive_name}.zip')
    with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_LZMA) as zipf:
        zipf.setpassword(password.encode('utf-8'))
        zipf.setencryption(pyzipper.WZ_AES, nbits=256)
        for file in files:
            zipf.write(file, os.path.basename(file))
            log_to_summary(file, archive_name)
    logging.info(f'Archive created: {archive_name}.zip with encryption.')

def format_creation_date(modified_date):
    return modified_date.strftime('%Y%m')

root_folder = os.getcwd()
client_clean_folder = os.path.join(root_folder, 'clientClean')
os.makedirs(client_clean_folder, exist_ok=True)

password = 'Xavier'

files_to_zip = {}

client_image_folder = os.path.join(root_folder, 'clientImage')
client_text_folder = os.path.join(root_folder, 'clientText')

for folder_name, folder_path in [('clientImage', client_image_folder), ('clientText', client_text_folder)]:
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        formatted_date = format_creation_date(modified_time)
        archive_suffix = '-img' if folder_name == 'clientImage' else '-txt'
        archive_name = f'{formatted_date}{archive_suffix}'
        files_to_zip.setdefault(archive_name, []).append(file_path)

for archive_name, files in files_to_zip.items():
    create_encrypted_zip(files, archive_name, password, client_clean_folder)

logging.info("Archiving and encryption process is complete for all files.")

# =============================================================================
# End of Section C (End of CTRL + / here)
# =============================================================================

# =============================================================================
# Section D - Script error handling (Start of CTRL + / here)
# =============================================================================

# Configure logging to write messages to 'summary.txt' in the current working directory
log_file_path = os.path.join(os.getcwd(), 'summary.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# FTP server credentials and directories
ftp_host = '127.0.0.1'  # The hostname or IP address of the FTP server
ftp_user = 'admin'  # The username for the FTP account
ftp_passwd = 'admin'  # The password for the FTP account
remote_folder = '/resource/serverClean'  # The remote folder to create on the FTP server
local_zip_folder = os.path.join(os.getcwd(), 'clientClean')  # Local folder with zip files


# Function to create a directory on the FTP server
def create_directory(ftp, directory):
    try:
        ftp.mkd(directory)
        logging.info(f"Created directory: {directory}")
    except error_perm as e:
        response_code = str(e).split(None, 1)[0]
        if response_code == '550':
            logging.info(f"Directory already exists: {directory}")
        else:
            logging.error(f"Error creating directory {directory}: {e}")


# Function to upload zip files to the FTP server
def upload_files(ftp):
    try:
        ftp.cwd(remote_folder)
    except error_perm as e:
        logging.error(f"Could not change to directory {remote_folder}: {e}")
        return

    for filename in os.listdir(local_zip_folder):
        if filename.endswith('.zip'):
            local_path = os.path.join(local_zip_folder, filename)
            with open(local_path, 'rb') as file:
                ftp.storbinary(f'STOR {filename}', file)
                logging.info(f"Uploaded file: {filename}")


# Function to test the connectivity of the FTP server
def test_ftp_connection(host, retries=2, delay=5):
    while retries > 0:
        try:
            with FTP(host) as ftp:
                logging.info("FTP server is reachable.")
                return ftp
        except Exception as e:
            logging.error(f"Server unavailable for file upload: {e}")
            retries -= 1
            if retries > 0:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
    return None


# Main function to handle FTP operations
def main():
    ftp = test_ftp_connection(ftp_host)
    if ftp is not None:
        try:
            ftp = FTP()
            ftp.connect(host=ftp_host, port=22)
            ftp.login(ftp_user, ftp_passwd)
            logging.info(f"Logged in to FTP server. Current working directory: {ftp.pwd()}")
            create_directory(ftp, remote_folder)
            upload_files(ftp)
            logging.info("File upload completed successfully.")
        except Exception as e:
            logging.error(f"FTP error: {e}")
        finally:
            ftp.quit()


# Run the main function
if __name__ == "__main__":
    main()

# =============================================================================
# End of Section D (End of CTRL + / here)
# =============================================================================

# =============================================================================
# Section E - Summary file (Start of CTRL + / here)
# =============================================================================

import datetime

current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

username = 'xavier'

log_filename = f"{current_datetime}_{username}.log"

logging.basicConfig(filename=log_filename,
                    level=logging.INFO,
                    format='%(asctime)s, xavier - INFO - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

activities = [
    "Downloading file from ftp done.",
    "File sorting done.",
    "Scan file for virus done.",
    "Archive file done.",
    "Ping ftp connectivity done.",
    "Upload zip file done."
]

for activity in activities:
    logging.info(activity)

# =============================================================================
# End of Section E (End of CTRL + / here)
# =============================================================================

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

# =============================================================================
# Section F - Test Task Scheduler (Start of CTRL + / here)
# =============================================================================

import datetime

current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

username = 'xavier'

log_filename = "Task_Scheduler.log"

logging.basicConfig(filename=log_filename,
                    level=logging.INFO,
                    format='%(asctime)s, xavier - INFO - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

activities = [
    'Task Scheduler ran successfully'
]

for activity in activities:
    logging.info(activity)

# =============================================================================
# End of Section F (End of CTRL + / here)
# =============================================================================
