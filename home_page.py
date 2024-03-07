import tkinter as tk
from tkinter import simpledialog

def home():
    choice = None
    def on_button_click():
        label.config(text="Button Clicked!")

    def quit_application():
        nonlocal choice
        result = simpledialog.askstring("Quit", "Enter a value before quitting:")
        if result is not None:
            choice = result
            window.destroy()

    # Create the main window
    window = tk.Tk()
    window.title("Button Example")

    # Calculate screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate window width and height
    window_width = 300
    window_height = 200

    # Calculate the x and y coordinates for the window to be centered
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set window size and position
    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Create a button
    button = tk.Button(window, text="Click Me", command=on_button_click, width=15, height=2)

    # Create a Quit button
    quit_button = tk.Button(window, text="Quit", command=quit_application, width=15, height=2)

    # Create a label to display the result
    label = tk.Label(window, text="", font=("Helvetica", 32, "bold"))

    # Add a label for "You Win"
    win_label = tk.Label(window, text="You Win", font=("Helvetica", 32, "bold"))

    # Use the grid geometry manager to position the elements
    button.grid(row=0, column=0, padx=5, pady=5)
    quit_button.grid(row=0, column=1, padx=5, pady=5)
    label.grid(row=1, column=0, columnspan=2, pady=10)
    win_label.grid(row=2, column=0, columnspan=2, pady=10)

    # Configure row and column weights to center elements
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    # Start the main event loop
    window.mainloop()

    return choice