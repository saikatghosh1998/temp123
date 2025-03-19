import zipfile
import os

ZIP_FILE_PATH = "huge_file.zip"  # Update with your ZIP file path
EXTRACT_PATH = "unzipped_folder"  # Where to extract files
STATUS_FILE = "unzipped_files.txt"  # Log file to track extracted files

def load_unzipped_files():
    """Reads the status file to get the list of already extracted files."""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return set(line.strip() for line in f.readlines())
    return set()

def save_unzipped_file(filename):
    """Writes a newly extracted file to the status file."""
    with open(STATUS_FILE, "a") as f:
        f.write(filename + "\n")

def extract_zip_resumable(zip_path, extract_to):
    """Extracts files from ZIP, skipping already extracted ones."""
    already_extracted = load_unzipped_files()  # Load progress

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        all_files = zip_ref.namelist()
        total_files = len(all_files)

        for index, file in enumerate(all_files):
            if file in already_extracted:  # Skip already extracted files
                print(f"Skipping {file} (already extracted)")
                continue

            try:
                zip_ref.extract(file, extract_to)
                save_unzipped_file(file)  # Mark as extracted
                print(f"[{index+1}/{total_files}] Extracted: {file}")
            except Exception as e:
                print(f"Error extracting {file}: {e}")
                break  # Stop if an error occurs

if __name__ == "__main__":
    extract_zip_resumable(ZIP_FILE_PATH, EXTRACT_PATH)
    print("Extraction complete!")
