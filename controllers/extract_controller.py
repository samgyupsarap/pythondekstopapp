import subprocess
import os
from tkinter import messagebox



def run_extract_script(batch_number, parent_folder_path, caseid_pattern):
    """Run the .pff extraction script based on the selected batch number and open it with the specified application."""
    # Construct the batch folder name
    batch_folder_name = f"{caseid_pattern}_Batch_{batch_number}"
    
    # Define the path to your .pff file located inside the batch folder
    pff_file_path = os.path.join(parent_folder_path, batch_folder_name, "extractData.pff")  # Assuming the file is named extractData.pff

    # Ensure the file exists before trying to run it
    if not os.path.isfile(pff_file_path):
        messagebox.showerror("File Not Found", f"The file {pff_file_path} does not exist.")
        return

    # Define the path to the application that opens the .pff file
    application_path = r"C:\Program Files (x86)\CSPro 8.0\CSEntry.exe" # Ensure this points to the actual executable file

    try:
        # Attempt to run the .pff file using the specified application
        print(f"Attempting to execute: {pff_file_path} with {application_path}")  # Debugging statement
        subprocess.Popen([application_path, pff_file_path])  # Open the .pff file with the specified application
        print(f"Successfully opened {pff_file_path} with {application_path}")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
