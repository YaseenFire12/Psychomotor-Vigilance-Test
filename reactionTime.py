import tkinter as tk
import time
import random

# Initialize the main application window
root = tk.Tk()
root.title("Psychomotor Vigilance Test")
root.geometry("600x600")
root.resizable(False, False)

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (600 / 2))
y_coordinate = int((screen_height / 2) - (600 / 2))
root.geometry(f"600x600+{x_coordinate}+{y_coordinate}")

# Create a canvas to draw the dot and display text
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()

# Initialize variables
dot = None
start_time = None
reaction_times = []
experiment_duration = 60  # 1 minute long
experiment_start_time = None
on_title_screen = True  # Flag to check if the title screen is active

def show_title_screen():
    """Display the title screen with instructions."""
    global on_title_screen
    on_title_screen = True
    canvas.delete("all")
    title_text = "Welcome to the Psychomotor Vigilance Test"
    instructions = "Right-click or Press Enter to start"
    canvas.create_text(300, 200, text=title_text, font=("Helvetica", 16))
    canvas.create_text(300, 300, text=instructions, font=("Helvetica", 12))
    # Bind right-click to start the experiment
    canvas.bind("<Button-3>", start_experiment)
    root.bind("<Return>", start_experiment)


def start_experiment(event=None):
    """Start the reaction time experiment."""
    global experiment_start_time, on_title_screen
    if on_title_screen:
        on_title_screen = False
        experiment_start_time = time.time()
        canvas.unbind("<Button-3>")  # Unbind right-click to prevent restarting
        canvas.unbind("<Return>")
        reset_experiment()

def show_dot():
    """Display the dot at the center of the canvas."""
    global dot, start_time
    if time.time() - experiment_start_time < experiment_duration:
        # Clear any existing dot
        canvas.delete("all")
        # Draw a new dot at the center
        dot = canvas.create_oval(290, 290, 310, 310, fill="red")
        start_time = time.time()
    else:
        end_experiment()

def hide_dot(event):
    """Handle the event when the dot is clicked or spacebar is pressed."""
    global dot, start_time
    if dot:
        reaction_time = (time.time() - start_time) * 1000  # in milliseconds
        reaction_times.append(reaction_time)
        canvas.delete(dot)
        dot = None
        # Schedule the next dot display after a random interval between 1 to 3 seconds
        root.after(random.randint(1000, 3000), show_dot)

def end_experiment():
    """Conclude the experiment and display the average reaction time."""
    global dot
    if dot:
        canvas.delete(dot)  # Remove the dot if it's still displayed
        dot = None
    if reaction_times:
        average_reaction_time = sum(reaction_times) / len(reaction_times)
        result_text = f"Average Reaction Time: {average_reaction_time:.2f} ms"
    else:
        result_text = "No reactions recorded."
    canvas.delete("all")
    canvas.create_text(300, 300, text=result_text, font=("Helvetica", 16))
    # Add a Retry button
    retry_button = tk.Button(root, text="Retry", command=reset_experiment)
    canvas.create_window(300, 340, window=retry_button)

def reset_experiment():
    global reaction_times, experiment_start_time
    # Reset variables
    reaction_times = []
    experiment_start_time = time.time()
    # Clear the canvas
    canvas.delete("all")
    # Start the experiment by showing the first dot after 1 second
    root.after(1000, show_dot)

# Bind spacebar press to hide_dot function
canvas.bind("<Button-1>", hide_dot)
root.bind("<space>", hide_dot)

# Display the title screen at the start
show_title_screen()

root.mainloop()
