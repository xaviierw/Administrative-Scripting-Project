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
