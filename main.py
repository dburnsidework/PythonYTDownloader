import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp
import threading
import os # I have imported sys and os so you can also use my downloader yipee!!!
import sys

# =============================================================
#
#
#               Daniel's multiplatform downloader
#
#
# =============================================================

def get_resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

ffmpeg_bin_path = get_resource_path("ffmpeg_bin")

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "No URL Provided")
        return

    # Gets user choices from GUI
    format_choice = format_var.get()
    quality_choice = quality_var.get()

    # Configures yt-dlp based on the GUI selection
    if format_choice == "MP3 (Audio)":
        opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        # Determine the height based on input
        if quality_choice == "High (1080p)":
            height = "1080"
        elif quality_choice == "Standard (720p)":
            height = "720"
        else: # Default Option
            height = "480"
        opts = {
            'format': f'bestvideo[height<={height}]+bestaudio/best'
        }

    # Common options, helped by AI
    opts.update({
        'outtmpl': f'{downloads_path}/%(title)s.%(ext)s',
        'noplaylist': True,
        'ffmpeg_location': ffmpeg_bin_path
    })

    # Run in a separate thread to avoid window freezing, helped by AI again
    def run():
        try:
            status_label.config(text="Status: Downloading...")
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            status_label.config(text="Status: Complete!")
            messagebox.showinfo("Success", "Download Finished!")
        except Exception as e:
            status_label.config(text="Status: Error")
            messagebox.showerror("Download Error", str(e))

    threading.Thread(target=run).start()

# === GUI Setup ===
root = tk.Tk()
root.title("Fast YT Downloader")
root.geometry("450x500")
root.configure(bg="#f0f0f0")

# Custom Styling
style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", padding=5)
style.configure("TButton", font=("Helvetica", 10, "bold"))

# Main Container (adds padding around the edges)
main_frame = tk.Frame(root, bg="#ffffff", padx=30, pady=30, highlightthickness=1, highlightbackground="#dddddd")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Title
tk.Label(main_frame, text="Video Downloader", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#333333").pack(pady=(0, 20))

# URL Input Section
tk.Label(main_frame, text="Paste URL below:", font=("Helvetica", 9), bg="#ffffff", fg="#666666").pack(anchor="w")
url_entry = tk.Entry(main_frame, width=40, font=("Helvetica", 10), bd=0, bg="#f9f9f9", highlightthickness=1, highlightbackground="#cccccc")
url_entry.pack(pady=(5, 15), ipady=5)

# Format Selection
tk.Label(main_frame, text="Choose Format:", font=("Helvetica", 9), bg="#ffffff", fg="#666666").pack(anchor="w")
format_var = tk.StringVar(value="MP4 (Video)")
format_menu = ttk.Combobox(main_frame, textvariable=format_var, state="readonly", width=37)
format_menu['values'] = ["MP4 (Video)", "MP3 (Audio)"]
format_menu.pack(pady=(5, 15))

# Quality Selection
tk.Label(main_frame, text="Select Max Quality:", font=("Helvetica", 9), bg="#ffffff", fg="#666666").pack(anchor="w")
quality_var = tk.StringVar(value="Standard (720p)")
quality_menu = ttk.Combobox(main_frame, textvariable=quality_var, state="readonly", width=37)
quality_menu['values'] = ["Low (480p)", "Standard (720p)", "High (1080p)"]
quality_menu.pack(pady=(5, 20))

# Download Button
download_btn = tk.Button(
    main_frame,
    text="START DOWNLOAD",
    command=download_video,
    bg="#28a745",
    fg="white",
    font=("Helvetica", 10, "bold"),
    activebackground="#218838",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    width=20,
)
download_btn.pack(pady=10, ipady=8)

# Status Label
status_label = tk.Label(main_frame, text="Status: Ready", font=("Helvetica", 9, "italic"), bg="#ffffff", fg="#007bff")
status_label.pack(pady=10)

# Credits (Small and subtle)
credits_label = tk.Label(root, text="Made by daniel (me!!)", font=("Helvetica", 8), bg="#f0f2f5", fg="#999999")
credits_label.pack(side="bottom", pady=10)

root.mainloop()
