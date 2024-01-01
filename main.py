import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pytube


class VideoDownloader:
    def __init__(self, root):
        self.link1 = None
        self.quality_var = None
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        self.root.title("YouTube Downloader")
        self.root.config(bg='#D3D3D3')

        self.create_widgets()

    def create_widgets(self):
        self.create_labels()
        self.create_entry()
        self.create_quality_dropdown()
        self.create_buttons()

    def create_labels(self):
        lb = tk.Label(self.root, text="Video download from YouTube", font='Arial,15,bold', bg='#D3D3D3')
        lb.pack(pady=15)

        lb1 = tk.Label(self.root, text="Video URL:", font='Arial,15,bold', bg='#D3D3D3')
        lb1.place(x=10, y=80)

        lb2 = tk.Label(self.root, text="Select Quality:", font='Arial,15,bold', bg='#D3D3D3')
        lb2.place(x=10, y=120)

    def create_entry(self):
        self.link1 = tk.StringVar()
        en1 = tk.Entry(self.root, textvariable=self.link1, font='Arial,15,bold', width=30)
        en1.place(x=200, y=80)

    def create_quality_dropdown(self):
        quality_options = ["Highest", "720p", "480p", "360p"]
        self.quality_var = tk.StringVar()
        quality_dropdown = ttk.Combobox(self.root, textvariable=self.quality_var, values=quality_options, state="readonly")
        quality_dropdown.set("Highest")
        quality_dropdown.place(x=200, y=120)

    def create_buttons(self):
        entry_width = 180  # Adjust this value based on the desired width of the entry widget

        btn1_width = entry_width
        btn1 = tk.Button(self.root, text="Download", font='Arial,10,bold', bd=4, command=self.download, width=btn1_width)
        btn1.place(x=330, y=170)

        btn2_width = entry_width // 2
        btn2 = tk.Button(self.root, text="Clean", font='Arial,10,bold', bd=4, command=self.reset, width=btn2_width)
        btn2.place(x=215, y=230)

        btn3_width = entry_width // 2
        btn3 = tk.Button(self.root, text="Exit", font='Arial,10,bold', bd=4, command=self.exit, width=btn3_width)
        btn3.place(x=385, y=230)

    def download(self):
        try:
            yt_link = self.link1.get()
            youtube_link = pytube.YouTube(yt_link)
            quality_str = self.quality_var.get()
            video = self.get_video_with_quality(youtube_link, quality_str)
            download_path = self.get_download_path()
            video.download(download_path)
            result_msg = f"The download is complete. Video saved to:\n{download_path}"
            messagebox.showinfo("Done", result_msg)
        except Exception as e:
            result_msg = f"Something went wrong.\nError: {str(e)}"
            messagebox.showerror("Error", result_msg)

    @staticmethod
    def get_video_with_quality(youtube_link, quality_str):
        if quality_str == "Highest":
            return youtube_link.streams.get_highest_resolution()
        elif quality_str == "720p":
            return youtube_link.streams.filter(res="720p").first()
        elif quality_str == "480p":
            return youtube_link.streams.filter(res="480p").first()
        elif quality_str == "360p":
            return youtube_link.streams.filter(res="360p").first()

    @staticmethod
    def get_download_path():
        return filedialog.askdirectory()

    def reset(self):
        self.link1.set("")

    def exit(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloader(root)
    root.mainloop()
