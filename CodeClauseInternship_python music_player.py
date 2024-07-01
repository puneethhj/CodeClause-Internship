import os
import tkinter as tk
from tkinter import filedialog
from pygame import mixer

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("300x200")

        self.playlist = []
        self.current_song_index = -1
        self.is_paused = False

        mixer.init()

        self.add_widgets()

    def add_widgets(self):
        """Add buttons and other widgets to the GUI."""
        self.play_button = tk.Button(self.root, text="Play", command=self.play_song)
        self.play_button.pack(pady=10)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_song)
        self.pause_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_song)
        self.stop_button.pack(pady=10)

        self.select_folder_button = tk.Button(self.root, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack(pady=10)

    def select_folder(self):
        """Select a folder and load all music files into the playlist."""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.playlist = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.mp3', '.wav'))]
            if self.playlist:
                self.current_song_index = 0
                self.play_song()

    def play_song(self):
        """Play the current song."""
        if self.is_paused:
            mixer.music.unpause()
            self.is_paused = False
        else:
            if self.playlist:
                mixer.music.load(self.playlist[self.current_song_index])
                mixer.music.play()
                self.root.after(100, self.check_music_end)

    def pause_song(self):
        """Pause the current song."""
        if mixer.music.get_busy():
            mixer.music.pause()
            self.is_paused = True

    def stop_song(self):
        """Stop the current song."""
        if mixer.music.get_busy():
            mixer.music.stop()

    def check_music_end(self):
        """Check if the current song has ended and play the next song."""
        if not mixer.music.get_busy() and not self.is_paused:
            self.current_song_index += 1
            if self.current_song_index < len(self.playlist):
                self.play_song()
            else:
                self.current_song_index = 0
        else:
            self.root.after(100, self.check_music_end)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
