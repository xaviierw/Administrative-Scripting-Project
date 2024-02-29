log_file_path = os.path.join(os.getcwd(), 'summary.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# FTP server credentials and directories
ftp_host = '127.0.0.1'  # The hostname or IP address of the FTP server
ftp_user = 'admin'  # The username for the FTP account
ftp_passwd = 'admin'  # The password for the FTP account
remote_folder = '/resource/serverClean'  # The remote folder to create on the FTP server
local_zip_folder = os.path.join(os.getcwd(), 'clientClean')  # Local folder with zip files

def test_ftp_connection(host, retries=2, delay=5):
    while retries > 0:
        try:
            with FTP(host) as ftp:
                return ftp
        except Exception as e:
            logging.error(f"Server unavailable for file upload: {e}")
            retries -= 1
            if retries > 0:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
    return None

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

# Main function to handle FTP operations
# Main function to handle FTP operations
def main():
    ftp = test_ftp_connection(ftp_host)
    if ftp is not None:
        try:
            ftp = FTP()
            ftp.connect(host=ftp_host, port=22)  # Assuming you have a specific reason to use port 22
            ftp.login(ftp_user, ftp_passwd)
            logging.info(f"Logged in to FTP server. Current working directory: {ftp.pwd()}")
            create_directory(ftp, remote_folder)
            upload_files(ftp)
            logging.info("File upload completed successfully.")
        except Exception as e:
            logging.error(f"FTP error: {e}")
        finally:
            if ftp is not None:  # Check if the ftp object is not None before calling quit
                try:
                    ftp.quit()
                except Exception as e:
                    logging.error(f"Error closing FTP connection: {e}")
    else:
        logging.error("FTP connection failed. No operations were performed.")



# Run the main function
if __name__ == "__main__":
    main()
