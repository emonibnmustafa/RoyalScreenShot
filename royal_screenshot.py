import tkinter as tk
import pyautogui
import keyboard
from PIL import ImageGrab, Image, ImageDraw
import threading
import os
import webbrowser
from datetime import datetime
import subprocess
from plyer import notification

# Settings
hotkey = "f9"
shape_choice = "rectangle"
save_folder = os.path.join(os.path.expanduser("~"), "Pictures", "Royal Screenshot")
os.makedirs(save_folder, exist_ok=True)

# App info
APP_VERSION = "1.0"
DEVELOPER = "Emon IbnMustafa"
GITHUB_URL = "https://github.com/emonibnmustafa/RoyalScreenshot"

# Create root window
root = tk.Tk()
root.title("Royal Screenshot")
root.geometry("300x360")
root.resizable(False, False)

# Only one popup at a time
popup_open = False

def choose_shape():
    global shape_choice, popup_open

    if popup_open:
        return  # Prevent multiple popups
    popup_open = True

    popup = tk.Toplevel()
    popup.title("Choose Screenshot Shape")
    popup.geometry("300x150")
    popup.attributes('-topmost', True)

    label = tk.Label(popup, text="Select the shape for your screenshot:", font=("Arial", 11))
    label.pack(pady=10)

    def select_rectangle():
        global shape_choice, popup_open
        shape_choice = "rectangle"
        popup.destroy()
        popup_open = False
        start_selection()

    def select_free():
        global shape_choice, popup_open
        shape_choice = "free"
        popup.destroy()
        popup_open = False
        start_selection()

    rectangle_button = tk.Button(popup, text="Rectangle 📏", bg="lightblue", font=("Arial", 11), command=select_rectangle)
    rectangle_button.pack(pady=5)

    free_button = tk.Button(popup, text="Free Selection 🖍️", bg="lightgreen", font=("Arial", 11), command=select_free)
    free_button.pack(pady=5)

def start_selection():
    root.withdraw()
    root.update()

    selector = tk.Toplevel()
    selector.attributes('-fullscreen', True)
    selector.attributes('-alpha', 0.3)
    selector.config(bg='grey')

    canvas = tk.Canvas(selector, cursor="cross", bg="grey")
    canvas.pack(fill="both", expand=True)

    rect = None
    points = []
    start_x = start_y = end_x = end_y = 0
    cancel_selection = False

    def on_mouse_down(event):
        nonlocal start_x, start_y, cancel_selection
        if event.num == 3:
            cancel_selection = True
            selector.destroy()
            root.deiconify()
            return
        start_x, start_y = event.x, event.y
        if shape_choice == "free":
            points.clear()
            points.append((event.x, event.y))

    def on_mouse_drag(event):
        nonlocal rect
        canvas.delete("rect")
        if shape_choice == "rectangle":
            rect = canvas.create_rectangle(
                start_x, start_y, event.x, event.y,
                outline='white', width=3, dash=(6, 4), tags="rect"
            )
        else:
            points.append((event.x, event.y))
            if len(points) > 1:
                canvas.create_line(
                    points[-2][0], points[-2][1],
                    points[-1][0], points[-1][1],
                    fill='white', width=3, dash=(6, 4)
                )

    def on_mouse_up(event):
        nonlocal end_x, end_y
        if cancel_selection:
            return
        end_x, end_y = event.x, event.y
        selector.destroy()

        full_screenshot = pyautogui.screenshot()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Screenshot_{timestamp}.png"
        filepath = os.path.join(save_folder, filename)

        if shape_choice == "rectangle":
            x1 = min(start_x, end_x)
            y1 = min(start_y, end_y)
            x2 = max(start_x, end_x)
            y2 = max(start_y, end_y)
            cropped = full_screenshot.crop((x1, y1, x2, y2))
        else:
            if not points:
                root.deiconify()
                return

            x_coords = [p[0] for p in points]
            y_coords = [p[1] for p in points]
            min_x, max_x = min(x_coords), max(x_coords)
            min_y, max_y = min(y_coords), max(y_coords)
            cropped = full_screenshot.crop((min_x, min_y, max_x, max_y))

            mask = Image.new('L', (max_x - min_x, max_y - min_y), 0)
            draw = ImageDraw.Draw(mask)
            draw.polygon([(x - min_x, y - min_y) for (x, y) in points], fill=255)

            result = Image.new('RGBA', (max_x - min_x, max_y - min_y))
            result.paste(cropped, (0, 0))
            result.putalpha(mask)
            cropped = result

        confirm_popup = tk.Toplevel()
        confirm_popup.title("Save Screenshot?")
        confirm_popup.geometry("250x150")
        confirm_popup.attributes('-topmost', True)

        lbl = tk.Label(confirm_popup, text="Save this screenshot?", font=("Arial", 12))
        lbl.pack(pady=15)

        def save_screenshot():
            cropped.save(filepath)
            confirm_popup.destroy()
            root.deiconify()

            notification.notify(
                title="Royal Screenshot",
                message=f"Screenshot saved!\nLocation:\n{os.path.dirname(filepath)}",
                app_name="Royal Screenshot",
                timeout=5
            )

        def cancel_screenshot():
            confirm_popup.destroy()
            root.deiconify()

        save_button = tk.Button(confirm_popup, text="Save", bg="lightgreen", font=("Arial", 11), command=save_screenshot)
        save_button.pack(pady=5)

        cancel_button = tk.Button(confirm_popup, text="Cancel", bg="lightcoral", font=("Arial", 11), command=cancel_screenshot)
        cancel_button.pack(pady=5)

    def on_key_press(event):
        nonlocal cancel_selection
        if event.keysym == 'Escape':
            cancel_selection = True
            selector.destroy()
            root.deiconify()

    canvas.bind("<Button-1>", on_mouse_down)
    canvas.bind("<Button-3>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)
    selector.bind("<Escape>", on_key_press)

def open_folder(path):
    subprocess.Popen(f'explorer "{path}"')

def open_image(path):
    subprocess.Popen(f'explorer "{path}"')

def open_github():
    webbrowser.open(GITHUB_URL)

def start_hotkey_listener():
    keyboard.add_hotkey(hotkey, choose_shape)
    keyboard.wait()

# --- Welcome GUI ---

welcome_label = tk.Label(root, text="Welcome to Royal Screenshot!", font=("Arial", 13, "bold"))
welcome_label.pack(pady=10)

version_label = tk.Label(root, text=f"Version: {APP_VERSION}", font=("Arial", 10))
version_label.pack()

developer_label = tk.Label(root, text=f"Developer: {DEVELOPER}", font=("Arial", 10))
developer_label.pack()

instructions_label = tk.Label(root, text="Press [F9] anytime\nto capture your screen.\n\nChoose shape, select area,\nand Save/Cancel.", font=("Arial", 10))
instructions_label.pack(pady=10)

github_button = tk.Button(root, text="View on GitHub", font=("Arial", 10), bg="lightblue", command=open_github)
github_button.pack(pady=5)

background_instructions = tk.Label(
    root,
    text="Please keep the app running in the background.\nMinimize it to work properly.\n(Do not close the app.)",
    font=("Arial", 10),
    justify="center"
)
background_instructions.pack(pady=10)

# Start hotkey listener in background
listener_thread = threading.Thread(target=start_hotkey_listener, daemon=True)
listener_thread.start()

# Start GUI loop
root.mainloop()
