import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from controllers.data_controller import handle_submit  # Import the new function


class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Finding CaseID")
        self.root.geometry("500x1000")
        self.root.resizable(False, False)

        # Load and set the background image
        self.bg_image = Image.open("./src/bg_py_app.png")  # Path to your background image
        self.bg_image = self.bg_image.resize((500, 1000), Image.LANCZOS)  # Resize image to fit the window
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas to hold the background image and widgets
        self.canvas = ctk.CTkCanvas(self.root, width=500, height=1000, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image_tk)

        # Consistent width for entry fields and buttons
        self.entry_width = 300  # Adjust the pixel width for entries and buttons

        # Create a label for CaseID (centered)
        self.canvas.create_text(250, 330, text="CaseID", font=("Helvetica", 16, "bold"), fill="black")

        # CaseID entry with white background
        self.caseid_entry = ctk.CTkEntry(
            self.canvas, font=("Helvetica", 18), width=self.entry_width, height=60,
            fg_color="white", text_color="black"
        )
        self.canvas.create_window(250, 380, window=self.caseid_entry)

        # Create a label for Number of Records (centered)
        self.canvas.create_text(250, 450, text="Number of Records per Batch", font=("Helvetica", 16, "bold"), fill="black")

        # Number of Records entry with white background
        self.records_entry = ctk.CTkEntry(
            self.canvas, font=("Helvetica", 18), width=self.entry_width, height=60,
            placeholder_text="Default: 1000", fg_color="white", text_color="black",
            placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 500, window=self.records_entry)

        # Submit button with custom style
        self.submit_button = ctk.CTkButton(
            self.canvas, text="Submit", font=("Helvetica", 20, "bold"), height=70, width=self.entry_width,
            fg_color="#0073c2", hover_color="#005ea6", text_color="white", command=self.submit
        )
        self.canvas.create_window(250, 600, window=self.submit_button)

    def submit(self):
        caseid_pattern = self.caseid_entry.get().strip()
        records_per_batch = self.records_entry.get().strip()

        # Call the handle_submit function from data_controller
        handle_submit(caseid_pattern, int(records_per_batch) if records_per_batch else 1000) 