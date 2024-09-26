import requests
from tkinter import messagebox, filedialog
from utils.file_utils import save_data_to_file, create_folder_if_not_exists, copy_from_copyfolder
from models.api_model import API_URL, API_COUNT_URL
from models.token_model import TokenStorage
import threading
import customtkinter as ctk
from concurrent.futures import ThreadPoolExecutor
import os
import time
from views.extract_view import ExtractView  # Import the ExtractView class

# Global variable to track the number of batches
num_batches = 0

def get_total_records(caseid_pattern):
    """Fetch the total number of records available from the custom API."""
    token = TokenStorage.get_token()
    url = f"{API_COUNT_URL}?caseidPattern={caseid_pattern}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        total_records = data.get('count', 0)
        return total_records if isinstance(total_records, int) else total_records.get('count', 0)
    except requests.RequestException as e:
        messagebox.showerror("API Error", f"Failed to fetch total records: {e}")
        return 0

def fetch_all_data(caseid_pattern, max_limit):
    """Fetch all data from the API based on the caseid_pattern."""
    token = TokenStorage.get_token()
    url = f"{API_URL}?caseidPattern={caseid_pattern}&limit={max_limit}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        caseids = [result['caseid'] for result in data.get('results', [])]

        return caseids
    except requests.RequestException as e:
        messagebox.showerror("API Error", f"Failed to fetch data: {e}")
        return None

def process_batches(parent_folder_path, caseid_pattern, records_per_batch, progress_label, progress_bar, progress_window, on_complete_callback):
    """Process batches based on the number of records per batch and total records in the API."""
    global num_batches

    # Create the main batch directory if it doesn't exist
    main_batch_folder = create_folder_if_not_exists(parent_folder_path, caseid_pattern)

    total_records = get_total_records(caseid_pattern)
    
    if total_records == 0:
        messagebox.showerror("No Data", "No records found for the given CaseID pattern.")
        return

    all_caseids = fetch_all_data(caseid_pattern, total_records)

    if not all_caseids:
        messagebox.showerror("No Data", "No records found for the given CaseID pattern.")
        return

    total_records = len(all_caseids)
    num_batches = (total_records + records_per_batch - 1) // records_per_batch

    fetch_batches(all_caseids, main_batch_folder, caseid_pattern, records_per_batch, progress_label, progress_bar, progress_window, on_complete_callback)

def fetch_batches(all_caseids, main_batch_folder, caseid_pattern, records_per_batch, progress_label, progress_bar, progress_window, on_complete_callback):
    """Handle the fetching of batches and show progress."""
    def save_batch(batch_no):
        start_index = (batch_no - 1) * records_per_batch
        end_index = min(start_index + records_per_batch, len(all_caseids))
        batch_caseids = all_caseids[start_index:end_index]

        subfolder_name = f"{caseid_pattern}_Batch_{batch_no}"
        batch_folder_path = create_folder_if_not_exists(main_batch_folder, subfolder_name)

        save_data_to_file(batch_folder_path, caseid_pattern, batch_no, batch_caseids)
        copy_from_copyfolder(batch_folder_path, caseid_pattern, batch_no)

        progress_label.configure(text=f"Completed Batch {batch_no}/{num_batches}")
        progress_bar.set(batch_no / num_batches)
        progress_window.update()  # Use the passed progress_window

    with ThreadPoolExecutor(max_workers=10) as executor:
        for batch_no in range(1, num_batches + 1):
            executor.submit(save_batch, batch_no)
            time.sleep(0.5)

    # Call the completion callback
    on_complete_callback()

def open_extract_view(num_batches, parent_folder_path, caseid_pattern):
    """Open the ExtractView in a new window after batch processing is complete."""
    extract_window = ctk.CTkToplevel()  # Create a new window
    extract_window.title("Extract View")
    extract_window.geometry("400x600")

    # Create an instance of ExtractView in the new window
    extract_view = ExtractView(extract_window, num_batches, parent_folder_path, caseid_pattern)  # Pass num_batches, parent_folder_path, and caseid_pattern
    extract_view.pack(expand=True, fill='both')

def handle_submit(caseid_pattern, records_per_batch):
    """Handle the submit logic from the main view."""
    folder_path = filedialog.askdirectory(title="Select Parent Directory")

    if not folder_path:
        messagebox.showwarning("No Directory Selected", "Please select a directory.")
        return

    total_records = get_total_records(caseid_pattern)

    if total_records == 0:
        messagebox.showerror("No Data", "No records found for the given CaseID pattern.")
        return

    global num_batches
    num_batches = (total_records + records_per_batch - 1) // records_per_batch

    confirm_message = f"This operation will generate {num_batches} batches, each with up to {records_per_batch} records.\n\nDo you want to proceed?"
    confirm = messagebox.askyesno("Confirm Batch Generation", confirm_message)

    if not confirm:
        return

    # Immediately show the progress window before starting the processing
    progress_window = ctk.CTkToplevel()
    progress_window.title("Fetching Data")
    progress_window.geometry("300x150")
    progress_window.grab_set()  # Make this window modal

    progress_label = ctk.CTkLabel(progress_window, text="Starting batch processing...")
    progress_label.pack(pady=10)

    progress_bar = ctk.CTkProgressBar(progress_window, width=250)
    progress_bar.pack(pady=10)
    progress_bar.set(0)

    # Function to update the progress and close the window
    def on_batches_complete():
        progress_label.configure(text="All batches completed!")
        progress_bar.set(1)
        progress_window.update()
        # Close the progress window after a delay
        progress_window.after(2000, lambda: (progress_window.destroy(), open_extract_view(num_batches, folder_path, caseid_pattern)))

    threading.Thread(target=process_batches, args=(folder_path, caseid_pattern, records_per_batch, progress_label, progress_bar, progress_window, on_batches_complete)).start()

# Main execution code or the main Tkinter app code
if __name__ == "__main__":
    root = ctk.CTk()  # Create the main window
    root.title("Main Application")
    root.geometry("600x400")

    # Example of how to trigger the handle_submit function
    caseid_pattern = "your_caseid_pattern"  # Replace with actual caseid pattern
    records_per_batch = 10  # Replace with your desired records per batch
    submit_button = ctk.CTkButton(root, text="Submit", command=lambda: handle_submit(caseid_pattern, records_per_batch))
    submit_button.pack(pady=20)

    root.mainloop()  # Start the Tkinter event loop  
