import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pygame
import threading
import time
from file_manager import FileManager

class MUSHRAApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.mushra_file_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                           title="Select MUSHRA File",
                                                           filetypes=(("Text files", "*.txt"),))
        self.title("Headphone Virtualizer and MUSHRA test")
        self.geometry("600x650")

        self.current_trial = 1
        self.scores = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}
        self.available_files = list(range(1, 6))  # Available file numbers (1-5)

        self.app_title = tk.Label(self, text="Listening Test Software", font=("Arial", 24, "bold"))
        self.app_title.pack(pady=20)

        self.instructions_label = tk.Label(self, text="Please rate the Basic Audio Quality of "
                                                      "the following using the scales provided.", font=("Arial", 12))
        self.instructions_label.pack(pady=10)
        # Scoring guide label
        self.scoring_guide_label = tk.Label(self, text="Scoring Guide:\n"
                                                       "100 - Excellent\n"
                                                       "80 - Good\n"
                                                       "60 - Fair\n"
                                                       "40 - Poor\n"
                                                       "20 - Bad\n"
                                                       "0 - Worst", font=("Arial", 10))
        self.scoring_guide_label.pack(pady=10)

        self.trial_label = tk.Label(self, text=f"Trial {self.current_trial} out of 5")
        self.trial_label.pack()

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack()

        self.buttons = {}
        button_texts = ['A', 'B', 'C', 'D', 'E']
        for button_text in button_texts:
            button_frame = tk.Frame(self.buttons_frame)
            button_frame.pack(side=tk.LEFT, padx=10)

            button = ttk.Button(button_frame, text=button_text,
                                command=lambda b=button_text: self.on_button_click(b))
            button.pack()

            slider = tk.Scale(button_frame, from_=100, to=0, orient=tk.VERTICAL, length=200)
            slider.pack()
            setattr(self, f"{button_text}_slider", slider)

        player_control_frame = tk.Frame(self)
        player_control_frame.pack(pady=10)

        self.play_button = ttk.Button(player_control_frame, text="Play", command=self.play_audio)
        self.play_button.grid(row=0, column=0, padx=5)

        self.pause_button = ttk.Button(player_control_frame, text="Pause", command=self.pause_audio)
        self.pause_button.grid(row=0, column=1, padx=5)

        self.stop_button = ttk.Button(player_control_frame, text="Stop", command=self.stop_audio)
        self.stop_button.grid(row=0, column=2, padx=5)

        self.loop_var = tk.BooleanVar()
        self.loop_checkbutton = ttk.Checkbutton(player_control_frame, text="Loop", variable=self.loop_var)
        self.loop_checkbutton.grid(row=0, column=3, padx=5)

        self.audio_slider = ttk.Scale(player_control_frame, from_=0, to=100,
                                      orient=tk.HORIZONTAL, length=400, command=self.update_audio_position)
        self.audio_slider.grid(row=1, column=0, columnspan=4, pady=10)

        # Next trial button
        self.next_button = ttk.Button(self, text="Next", command=self.next_trial)
        self.next_button.pack(pady=10)

        # Initialize pygame mixer
        pygame.mixer.init()

        # Show file dialog to upload MUSHRA.txt at startup
        self.file_manager = FileManager()
        self.file_manager.upload_mushra_file(self)

        # Randomly assign files to buttons when the trial screen opens
        self.file_manager.randomize_files(self)

        # Start a thread to continuously update the playback slider position
        self.slider_thread = threading.Thread(target=self.update_slider_position, daemon=True)
        self.slider_thread.start()

    def on_button_click(self, button_text):
        self.file_manager.on_button_click(self, button_text)

    def play_audio(self):
        pygame.mixer.music.unpause()

    def pause_audio(self):
        pygame.mixer.music.pause()

    def stop_audio(self):
        pygame.mixer.music.stop()

    def update_audio_position(self, value):
        pass

    def next_trial(self):
        self.file_manager.next_trial(self)

    def end_screen(self):
        end_screen = tk.Toplevel()
        end_screen.title("End Screen")
        end_label = tk.Label(end_screen, text="Thank you for answering. Please proceed to the Method of Adjustment.")
        end_label.pack(pady=20)
        close_button = ttk.Button(end_screen, text="Close", command=end_screen.destroy)
        close_button.pack(pady=10)

    def update_slider_position(self):
        while True:
            if pygame.mixer.music.get_busy():
                # Get current playback position
                current_pos = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
                # Get length of audio
                audio_file = os.path.join(os.getcwd(), "pm", f"{self.current_trial}.wav")
                try:
                    length = pygame.mixer.Sound(audio_file).get_length()
                except pygame.error:
                    length = 0
                # Calculate slider position
                slider_position = (current_pos / length) * 100 if length != 0 else 0
                # Update slider position
                self.audio_slider.set(slider_position)
            time.sleep(0.1)  # Update slider position every 0.1 seconds
