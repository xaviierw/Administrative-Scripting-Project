# =============================================================================
# Section C - Encrypting and zipping of files (Start of CTRL + / here)
#  SETUP: Logging configuration
# =============================================================================

import datetime

# Configure the logging to write messages to 'summary.txt' in the current working directory.
# The format for messages will be just the message itself with no level or time prefix.
log_file_path = os.path.join(os.getcwd(), 'summary.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(message)s')

# Define a function to log the summary of file addition to the zip file.
def log_to_summary(file_path, archive_name):
    # Extract the year and month from the archive name
    year = archive_name[:4]
    month = archive_name[4:6]
    # Convert the month number to the abbreviated month name
    month_name = datetime.datetime.strptime(month, "%m").strftime("%b")
    # Format the log message with the file path, month name, year, and archive name
    log_message = f"{file_path} created on {month_name} {year} archive to {archive_name}.zip"
    # Log the formatted message
    logging.info(log_message)

# Define a function to create an encrypted zip file with the given files.
def create_encrypted_zip(files, archive_name, password, output_folder):
    # Construct the full path for the zip file
    zip_path = os.path.join(output_folder, f'{archive_name}.zip')
    # Open a new zip file with AES encryption
    with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_LZMA) as zipf:
        # Set the password for the zip file
        zipf.setpassword(password.encode('utf-8'))
        # Choose AES encryption
        zipf.setencryption(pyzipper.WZ_AES, nbits=256)
        # Loop through the list of files to add to the zip file
        for file in files:
            # Add each file to the zip file
            zipf.write(file, os.path.basename(file))
            # Log the addition of each file
            log_to_summary(file, archive_name)
    # Log the completion of the zip file creation
    logging.info(f'Archive created: {archive_name}.zip with encryption.')

# Define a function to format the creation date of files for use in the zip file name.
def format_creation_date(modified_date):
    # Return a string with the formatted year and month
    return modified_date.strftime('%Y%m')

# Set the root folder to the current working directory of the script
root_folder = os.getcwd()
# Define the path for the directory where the zip files will be stored
client_clean_folder = os.path.join(root_folder, 'clientClean')
# Create the directory if it doesn't exist
os.makedirs(client_clean_folder, exist_ok=True)

# Define the password for encrypting the zip files
password = 'Xavier'
# Initialize a dictionary to hold the grouping of files by their archive name
files_to_zip = {}

# Define the folders for images and text files relative to the root folder
client_image_folder = os.path.join(root_folder, 'clientImage')
client_text_folder = os.path.join(root_folder, 'clientText')

# Loop over both folders to process files
for folder_name, folder_path in [('clientImage', client_image_folder), ('clientText', client_text_folder)]:
    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        # Get the full path of the file
        file_path = os.path.join(folder_path, filename)
        # Get the modified time of the file and convert it to a datetime object
        modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        # Format the date to year and month for use in the archive name
        formatted_date = format_creation_date(modified_time)
        # Determine the suffix for the archive name based on the folder
        archive_suffix = '-img' if folder_name == 'clientImage' else '-txt'
        # Construct the archive name
        archive_name = f'{formatted_date}{archive_suffix}'
        # Add the file to the list of files for this archive name
        files_to_zip.setdefault(archive_name, []).append(file_path)

# Loop over each archive name and the associated files
for archive_name, files in files_to_zip.items():
    # Call the function to create an encrypted zip file with the collected files
    create_encrypted_zip(files, archive_name, password, client_clean_folder)

# Log that the entire archiving and encryption process is complete
logging.info("Archiving and encryption process is complete for all files.")

# =============================================================================
# End of Section C (End of CTRL + / here)
# =============================================================================
