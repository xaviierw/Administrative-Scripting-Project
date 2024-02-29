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
# =============================================================================
