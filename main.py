import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from pathlib import Path
from shutil import copy2
from pygame import mixer
import os


current_dir = os.getcwd()

RYTHMWAVE_LIBARY_PATH = current_dir + "/Rythmwave_Library"
RYTHMWAVE_ASSETS_PATH = current_dir + "/assets/"
RYTHMWAVE_ICONS_PATH = RYTHMWAVE_ASSETS_PATH + "icons/"
RYTHMWAVE_LOGO = RYTHMWAVE_ASSETS_PATH + "Rythmwave.png"

class AboutUsWindow(tk.Toplevel):
    alive = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.config(bg="black")
        self.title("About us")
        self.aboutUsFrame = ttk.Frame(width=400, height=200, borderwidth=0)
        self.setup_custom_style()
        self.setup_dev_names()

        self.focus()
        self.__class__.alive = True

    def destroy(self):
        self.__class__.alive = False

        return super().destroy()

    def setup_dev_names(self):
        dev_names = {
            "Abhid Sheheer": "heart",
            "Mihal P.L" : "coffee_mug",
            "Akash M.D": "cross",
            "Mubeen Rahman": "pirate",
        }
        row = 1
        for name, cursor in dev_names.items():
            row += 1
            ttk.Button(self,
                text=name,
                command=None,
                cursor=cursor,
                style="A.TButton"
            ).grid(column=0, row=row, pady=20, padx=50)

    def setup_custom_style(self):
        self.AStyle = ttk.Style()
        self.AStyle.configure(
            "A.TButton",
            font=('Arial', 30, 'bold'),
            foreground="gray",
            background="black",
            borderwidth="0"
        )
        self.AStyle.map("A.TButton",
            foreground=[("active", "!disabled", "purple")],
            background=[("active", "black")]
        )

class PlayMusicWindow(tk.Toplevel):
    WHITE = "#FFFFFF"
    PURPLE = "#3C1DC6"
    DARK_GRAY = "#333333"
    LIGHT_PURPLE = "#CFC7F8"

    alive = False
    paused = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(width=352, height=255, bg=self.__class__.WHITE)
        self.title("Playing music")
        self.resizable(0,0)

        self.left_frame = tk.Frame(self, width=150, height=150, bg=self.__class__.WHITE, borderwidth=0)
        self.left_frame.grid(row=0, column=0, pady=1)

        self.right_frame = tk.Frame(self, width=250, height=150, bg=self.__class__.DARK_GRAY, borderwidth=0)
        self.right_frame.grid(row=0, column=1, pady=0)

        self.down_frame = tk.Frame(self, width=400, height=100, bg=self.__class__.LIGHT_PURPLE, borderwidth=0)
        self.down_frame.grid(row=1, column=0, columnspan=3, padx=0, pady=1)

        self.setup_widgets()

        self.focus()        
        self.__class__.alive = True

    def destroy(self):
        self.__class__.alive = False

        return super().destroy()

    def setup_widgets(self):
        self.listbox = tk.Listbox(self.right_frame, selectmode=tk.SINGLE, font=("Arial 9 bold"), width=33, bg=self.__class__.DARK_GRAY, fg=self.__class__.WHITE)
        self.listbox.grid(row=0, column=0)

        self.scroll = tk.Scrollbar(self.right_frame)
        self.scroll.grid(row=0, column=1)

        self.listbox.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.listbox.yview)

        self.show_all_music()
        self.listbox.select_set(first=0)

        music_icon_image = Image.open(RYTHMWAVE_ICONS_PATH + "music.png")
        resized_music_icon = music_icon_image.resize((150,110))
        self.music_icon_image = ImageTk.PhotoImage(resized_music_icon)
        self.music_icon = tk.Label(self.left_frame, image=self.music_icon_image, padx=10, height=100, bg=self.__class__.WHITE)
        self.music_icon.place(x=2, y=15)

        play_icon_image = Image.open(RYTHMWAVE_ICONS_PATH + "play.png")
        resized_play_icon = play_icon_image.resize((30,30))
        self.resized_play_image = ImageTk.PhotoImage(resized_play_icon)

        self.play_icon = tk.Button(self.down_frame, image=self.resized_play_image, padx=10, height=40, width=40, bg=self.__class__.WHITE, command=self.play_music)
        self.play_icon.place(x=60+28, y=35)

        previous_icon_image = Image.open(RYTHMWAVE_ICONS_PATH + "previous.png")
        resized_previous_icon = previous_icon_image.resize((30,30))
        self.resized_previous_image = ImageTk.PhotoImage(resized_previous_icon)
        self.previous_icon = tk.Button(self.down_frame, image=self.resized_previous_image, padx=10, height=40, width=40, bg=self.__class__.WHITE, command=self.previous_music)
        self.previous_icon.place(x=106+28, y=35)

        pause_icon_image = Image.open(RYTHMWAVE_ICONS_PATH + "pause.png")
        resized_pause_icon = pause_icon_image.resize((30,30))
        self.resized_pause_image = ImageTk.PhotoImage(resized_pause_icon)

        resume_icon_image = Image.open(RYTHMWAVE_ICONS_PATH + "resume.png")
        resized_resume_icon = resume_icon_image.resize((30, 30))
        self.resized_resume_image = ImageTk.PhotoImage(resized_resume_icon)

        self.pause_icon = tk.Button(self.down_frame, image=self.resized_pause_image, padx=10, height=40, width=40, bg=self.__class__.WHITE, command=self.pause_music)
        self.pause_icon.place(x=152+28, y=35)

        next_icon_image = Image.open(RYTHMWAVE_ICONS_PATH + "next.png")
        resized_next_icon = next_icon_image.resize((30,30))
        self.resized_next_image = ImageTk.PhotoImage(resized_next_icon)
        self.next_icon = tk.Button(self.down_frame, image=self.resized_next_image, padx=10, height=40, width=40, bg=self.__class__.WHITE, command=self.next_music)
        self.next_icon.place(x=198+28, y=35)

        stop_icon_image = Image.open(RYTHMWAVE_ICONS_PATH + "stop.png")
        resized_stop_icon = stop_icon_image.resize((30,30))
        self.resized_stop_image = ImageTk.PhotoImage(resized_stop_icon)
        self.stop_icon = tk.Button(self.down_frame, image=self.resized_stop_image, padx=10, height=40, width=40, bg=self.__class__.WHITE, command=self.stop_music)
        self.stop_icon.place(x=244+28, y=35)

        self.music_info = tk.Label(self.down_frame, text="Choose a music", font=("Ivy 10"), width=400, height=1, padx=10, bg=self.__class__.WHITE, fg=self.__class__.DARK_GRAY, anchor=tk.NW)
        self.music_info.place(x=0, y=1)


    def play_music(self):
        self.reset_pause_button()
        selected_music = self.listbox.get(tk.ACTIVE)
        self.music_info["text"] = selected_music
        mixer.music.load(selected_music)
        mixer.music.play()

    def pause_music(self):
        if not self.__class__.paused:
            mixer.music.pause()
            self.__class__.paused = True
            self.pause_icon.config(image=self.resized_resume_image)
        else: 
            mixer.music.unpause()
            self.__class__.paused = False
            self.pause_icon.config(image=self.resized_pause_image)

    def show_all_music(self):
        os.chdir(RYTHMWAVE_LIBARY_PATH)
        self.musics = os.listdir()
        for i in self.musics:
            self.listbox.insert(tk.END, i)

    def stop_music(self):
        self.reset_pause_button()
        self.music_info["text"] = "Choose a music"
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(first=0)
        mixer.music.stop()

    def next_music(self):
        self.music_control("next")

    def previous_music(self):
        self.music_control("previous")

    def music_control(self, action):
        self.reset_pause_button()
        current_music_index, *_ = self.listbox.curselection()

        music_index = current_music_index + 1 if action == "next" else current_music_index - 1
        music = self.musics[music_index]
        
        self.listbox.select_clear(0, tk.END)
        self.listbox.select_set(music_index, last=None)
        self.listbox.activate(music_index)
        self.music_info["text"] = music

        mixer.music.load(music)
        mixer.music.play()

    def reset_pause_button(self):
        if self.__class__.paused:
            self.__class__.paused == False
            self.pause_icon.config(image=self.resized_pause_image)


class RythmwaveMainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_rythmwave_library()

        self.config(bg="black")
        self.title("Rythm Wave")
        self.mainFrame = ttk.Frame(self, width=500, height=500, borderwidth=0)
        self.resizable(0,0)
        self.setup_custom_style()
        self.setup_widgets()

    def open_play_music_window(self):
        if not PlayMusicWindow.alive:
            self.play_music_window = PlayMusicWindow()

    def open_about_us_window(self):
        if not AboutUsWindow.alive:
            self.about_us_window = AboutUsWindow()

    def file_picker(self):
        file_path = filedialog.askopenfilename(
            initialdir="~/Downloads/Music",
            filetypes=[("MP3", ".mp3")],
            multiple=False
        )
        if file_path:
            file_name = file_path.split("/")[-1]
            if not Path(RYTHMWAVE_LIBARY_PATH + "/" + file_name).is_file():
                copy2(file_path, RYTHMWAVE_LIBARY_PATH)

    def setup_rythmwave_library(self):
        if not Path(RYTHMWAVE_LIBARY_PATH).is_dir():
            Path.mkdir(RYTHMWAVE_LIBARY_PATH)

    def setup_custom_style(self):
        self.MStyle = ttk.Style()
        self.MStyle.configure(
            "M.TButton",
            font=('Arial', 25, 'bold'),
            foreground="gray",
            background="black",
            borderwidth="0"
        )
        self.MStyle.map("M.TButton",
            foreground=[("active", "!disabled", "white")],
            background=[("active", "black")]
        )

    def setup_widgets(self):
        logo_image = Image.open(RYTHMWAVE_LOGO)
        resized_logo = logo_image.resize((350, 260))
        self.logo = ImageTk.PhotoImage(resized_logo)
        self.logo_label = ttk.Label(self, image=self.logo, borderwidth=0)
        self.logo_label.grid(column=0, row=0, padx=5, pady=30)

        self.add_music_btn =  ttk.Button(
            self,
            text="Add Music",
            command=self.file_picker,
            cursor="hand2",
            style="M.TButton"
        ).grid(column=0, row=1, pady=5)

        self.play_music_btn = ttk.Button(
            self,
            text="Play Music",
            command=self.open_play_music_window,
            cursor="hand2",
            style="M.TButton"
        )
        self.play_music_btn.grid(column=0, row=2, pady=5)

        self.about_us_btn = ttk.Button(self,
            text="About us",
            command=self.open_about_us_window,
            cursor="star",
            style="M.TButton"
        ).grid(column=0, row=3, pady=50)


mixer.init()

main_window = RythmwaveMainWindow()
main_window.mainloop()