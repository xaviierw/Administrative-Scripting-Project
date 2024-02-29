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
