import customtkinter as ctk
import yt_dlp
import os
import threading

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "%(title)s.%(ext)s")
app = ctk.CTk()

app.geometry("600x400")
app.title("Youtube Downloader")

entry = ctk.CTkEntry(app, placeholder_text="Enter Youtube URL", width=300)
entry.pack(pady=20)

progressbar = ctk.CTkProgressBar(app, orientation="horizontal", width=300)
progressbar.set(0)
progressbar.pack(pady=10)

status_label = ctk.CTkLabel(app, text="")
status_label.pack(pady=5)

def my_hook(d):
    if d['status'] == 'downloading':
        precent_str = d.get('_percent_str', '0%').strip().replace('%','')
        try:
            percent = float(precent_str) / 100
            progressbar.set(percent)
            status_label.configure(text=f"{d.get('_percent.str', '').strip()} - {d.get('_speed_str', '')}")
            app.update_idletasks
        except ValueError:
            pass
    elif d['status'] == 'finished':
        status_label.configure(text="✅ Download complete!")
        progressbar.set(1.0)


def run_download():
    url = entry.get()
    ydl_opts = {
        'outtmpl': desktop_path,
        "progress_hooks": [my_hook]
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print("Error", e)

def get_text():
    progressbar.set(0)
    status_label.configure(text="Starting...")
    thread = threading.Thread(target=run_download)
    thread.start()

button = ctk.CTkButton(app, text="Download", command=get_text)
button.pack(pady=20)

app.mainloop()
