import customtkinter as ctk
from PIL import Image, ImageTk
from controllers.extract_controller import run_extract_script

ctk.set_appearance_mode("light")

class ExtractView:
    def __init__(self, root, max_batches, parent_folder_path, caseid_pattern):
        self.root = root
        self.root.title("Extract View")
        self.root.geometry("500x1000")
        self.root.resizable(False, False)
        
        # Store the maximum number of batches, parent folder path, and caseid_pattern
        self.max_batches = max_batches
        self.parent_folder_path = parent_folder_path
        self.caseid_pattern = caseid_pattern  # Store the caseid_pattern

        # Load and set the background image
        self.bg_image = Image.open("./src/bg_py_app.png")  # Path to your background image
        self.bg_image = self.bg_image.resize((500, 1000), Image.LANCZOS)  # Resize image to fit the window
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas to hold the background image and widgets
        self.canvas = ctk.CTkCanvas(self.root, width=500, height=1000, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image_tk)

        # Create a label for the input field with a custom color for the text
        self.canvas.create_text(250, 350, text="Enter a Batch Number", font=("Helvetica", 20, "bold"), fill="black")

        # Number input field with up and down buttons
        self.number_var = ctk.IntVar(value=1)  # Initialize the number variable with a default of 1

        # Create a frame to hold the entry and buttons
        self.number_frame = ctk.CTkFrame(self.canvas, fg_color="white")  # Frame background color
        self.canvas.create_window(250, 450, window=self.number_frame)

        # Create an entry to display the number with customized colors
        self.number_entry = ctk.CTkEntry(
            self.number_frame, textvariable=self.number_var, font=("Helvetica", 18), width=100, height=60,
            fg_color="white",  # Entry background color
            text_color="black",  # Entry text color
            border_color="gray",  # Border color for the entry field
            corner_radius=10  # Rounded corners for a softer look
        )
        self.number_entry.pack(side='left', padx=(0, 10))  # Add some padding to the right

        # Create buttons to increase and decrease the number with customized colors
        self.increment_button = ctk.CTkButton(
            self.number_frame, text="▲", font=("Helvetica", 18), command=self.increment_number, width=50, height=50,
            fg_color="#0073c2",  # Button background color
            text_color="white",  # Button text color
            hover_color="#005ea6",  # Hover color for the button
            background_corner_colors=["#0073c2", "#0073c2", "#0073c2", "#0073c2"],  # Button corner colors
            corner_radius=10  # Rounded corners for consistency
        )
        self.increment_button.pack(side='left')  # Place button to the right of the entry

        self.decrement_button = ctk.CTkButton(
            self.number_frame, text="▼", font=("Helvetica", 18), command=self.decrement_number, width=50, height=50, 
            fg_color="#0073c2",  # Button background color
            text_color="white",  # Button text color
            hover_color="#005ea6",  # Hover color for the button
            background_corner_colors=["#0073c2", "#0073c2", "#0073c2", "#0073c2"],  # Button corner colors
            corner_radius=10  # Rounded corners for consistency
        )
        self.decrement_button.pack(side='left')  # Place button to the right of the entry

        # Button to confirm the input with customized colors
        self.confirm_button = ctk.CTkButton(
            self.canvas, text="Confirm", font=("Helvetica", 20, "bold"), height=70, width=200,
            fg_color="#0073c2",  # Button background color
            hover_color="#005ea6",  # Button hover color
            text_color="white",  # Button text color
            command=self.confirm_input, 
            background_corner_colors=["#0073c2", "#0073c2", "#0073c2", "#0073c2"],  # Button corner colors
            corner_radius=10  # Rounded corners for consistency
        )
        self.canvas.create_window(250, 550, window=self.confirm_button)

    def increment_number(self):
        """Increment the number in the entry field, respecting the max_batches limit."""
        current_value = self.number_var.get()
        if current_value < self.max_batches:  # Ensure we don't exceed the maximum
            self.number_var.set(current_value + 1)  # Increase the number by 1

    def decrement_number(self):
        """Decrement the number in the entry field, ensuring it doesn't go below 1."""
        current_value = self.number_var.get()
        if current_value > 1:  # Ensure we don't go below 1
            self.number_var.set(current_value - 1)  # Decrease the number by 1

    def confirm_input(self):
        """Handle the confirm button action."""
        number = self.number_var.get()
        if 1 <= number <= self.max_batches:
            print(f"Confirmed batch number: {number}")  # Replace this with the desired action
            # Call the extract controller to run the extract.pff for the selected batch
            run_extract_script(number, self.parent_folder_path, self.caseid_pattern)  # Pass the caseid_pattern
        else:
            ctk.CTkMessageBox.showwarning("Invalid Input", f"Please enter a number between 1 and {self.max_batches}.")
