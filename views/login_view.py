import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox

class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Login")

        # Set a fixed window size
        self.root.geometry("500x1000")
        self.root.resizable(False, False)  # Prevent resizing

        # Load and set the background image
        self.bg_image = Image.open("./src/bg_py_app.png")  # Path to your image file
        self.bg_image = self.bg_image.resize((500, 1000), Image.LANCZOS)  # Resize image using LANCZOS filter
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas and add the background image
        self.canvas = ctk.CTkCanvas(self.root, width=500, height=1000, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image_tk)

        # Define width for consistency
        self.entry_width = 280  # Adjust the pixel width for entries

        # Center the login label
        self.canvas.create_text(250, 350, text="Login", font=("Helvetica", 30, "bold"), fill="black")

        # Username entry with white background
        self.username_entry = ctk.CTkEntry(
            self.canvas, font=("Helvetica", 18), width=self.entry_width, height=60,
            placeholder_text="Enter username", fg_color="white",  # White background
            text_color="black",
            placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 430, window=self.username_entry)

        # Password entry with white background
        self.password_entry = ctk.CTkEntry(
            self.canvas, show="*", font=("Helvetica", 18), width=self.entry_width, height=60,
            placeholder_text="Enter password", fg_color="white",  # White background
            text_color="black",
            placeholder_text_color="#4d4949"
        )
        self.canvas.create_window(250, 500, window=self.password_entry)

        # Login button with updated styles
        self.login_button = ctk.CTkButton(
            self.canvas,
            text="Login",
            height=70,
            command=self.handle_login,
            font=("Helvetica", 20, "bold"),
            width=self.entry_width,
            fg_color="#0073c2",  # Button background color
            hover_color="#448ec2",  # Hover background color
            text_color="white", # Text color
            border_color="#000000",
            
        )
        self.canvas.create_window(250, 580, window=self.login_button)

        # Bind focus events for username and password entries (move this after widget creation)
        self.username_entry.bind("<FocusIn>", self.on_focus_in_username)
        self.username_entry.bind("<FocusOut>", self.on_focus_out_username)
        self.password_entry.bind("<FocusIn>", self.on_focus_in_password)
        self.password_entry.bind("<FocusOut>", self.on_focus_out_password)

    def on_focus_in_username(self, event):
        # Change the border color when username entry gains focus
        self.username_entry.configure(border_color="#0073c2")

    def on_focus_out_username(self, event):
        # Reset the border color when username entry loses focus
        self.username_entry.configure(border_color="black")

    def on_focus_in_password(self, event):
        # Change the border color when password entry gains focus
        self.password_entry.configure(border_color="#0073c2")

    def on_focus_out_password(self, event):
        # Reset the border color when password entry loses focus
        self.password_entry.configure(border_color="black")

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            self.on_login_success(username, password)
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")


if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginView(root, lambda u, p: print(f"Logged in with {u} and {p}"))
    root.mainloop()
