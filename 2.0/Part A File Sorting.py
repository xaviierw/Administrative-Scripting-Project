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
