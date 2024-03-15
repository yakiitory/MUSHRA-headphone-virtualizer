# audio_player.py

import os
import time
import tkinter as tk
from tkinter import ttk  # Import ttk from tkinter
import pygame


class AudioPlayer:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

        self.play_button = ttk.Button(parent_frame, text="Play", command=self.play_audio)
        self.play_button.grid(row=0, column=0, padx=5)

        self.pause_button = ttk.Button(parent_frame, text="Pause", command=self.pause_audio)
        self.pause_button.grid(row=0, column=1, padx=5)

        self.stop_button = ttk.Button(parent_frame, text="Stop", command=self.stop_audio)
        self.stop_button.grid(row=0, column=2, padx=5)

        self.loop_var = tk.BooleanVar()
        self.loop_checkbutton = ttk.Checkbutton(parent_frame, text="Loop", variable=self.loop_var)
        self.loop_checkbutton.grid(row=0, column=3, padx=5)

        self.audio_slider = ttk.Scale(parent_frame, from_=0, to=100,
                                      orient=tk.HORIZONTAL, length=400, command=self.update_audio_position)
        self.audio_slider.grid(row=1, column=0, columnspan=4, pady=10)

        self.current_trial = 1

    def play_audio(self):
        pygame.mixer.music.unpause()

    def pause_audio(self):
        pygame.mixer.music.pause()

    def stop_audio(self):
        pygame.mixer.music.stop()

    def update_audio_position(self, value):
        pass

    def update_slider_position(self, app_instance):
        while True:
            if pygame.mixer.music.get_busy():
                # Get current playback position
                current_pos = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
                # Get length of audio
                audio_file = os.path.join(os.getcwd(), "pm", f"{app_instance.current_trial}.wav")
                try:
                    length = pygame.mixer.Sound(audio_file).get_length()
                except pygame.error:
                    length = 0
                # Calculate slider position
                slider_position = (current_pos / length) * 100 if length != 0 else 0
                # Update slider position
                app_instance.audio_slider.set(slider_position)
            time.sleep(0.1)  # Update slider position every 0.1 seconds
