# file_manager.py

import os
import random
import tkinter as tk
from tkinter import ttk  # Import ttk from tkinter
import pygame


class FileManager:
    def upload_mushra_file(self, app_instance):
        if app_instance.mushra_file_path:
            with open(app_instance.mushra_file_path, 'r') as f:
                mushra_text = f.read()
                print("MUSHRA File Contents:")
                print(mushra_text)

    def on_button_click(self, app_instance, button_text):
        print(f"Button {button_text} clicked.")
        # Check if a file has already been assigned to the button
        if app_instance.scores[button_text] == 0:
            # Randomly choose a file for A-E if not already assigned
            file_number = random.choice(app_instance.available_files)
            app_instance.available_files.remove(file_number)  # Remove the selected file number from available_files
            file_path = os.path.join(os.getcwd(), "eq", f"{file_number}.txt")
            print(f"Reading contents of file: {file_path}")
            try:
                with open(file_path, 'r') as f:
                    new_contents = f.read()
                    print("Contents of the file:")
                    print(new_contents)
                    # Write the contents to the uploaded MUSHRA.txt file
                    self.write_to_mushra_file(new_contents, app_instance.mushra_file_path)
                    print("Contents written to MUSHRA.txt")
                    # Store the file used for the button
                    app_instance.scores[button_text] = f"{file_number}.txt"
            except FileNotFoundError:
                print(f"File {file_path} not found.")
        else:
            # Replace the contents of MUSHRA.txt with the file assigned to the button
            file_number = int(app_instance.scores[button_text].split('.')[0])
            file_path = os.path.join(os.getcwd(), "eq", f"{file_number}.txt")
            print(f"Reading contents of file: {file_path}")
            try:
                with open(file_path, 'r') as f:
                    new_contents = f.read()
                    print("Contents of the file:")
                    print(new_contents)
                    # Write the contents to the uploaded MUSHRA.txt file
                    self.write_to_mushra_file(new_contents, app_instance.mushra_file_path)
                    print("Contents written to MUSHRA.txt")
            except FileNotFoundError:
                print(f"File {file_path} not found.")

        # Play audio associated with the button
        audio_file = os.path.join(os.getcwd(), "pm", f"{app_instance.current_trial}.wav")
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

    def write_to_mushra_file(self, contents, file_path):
        # Write the contents to the uploaded MUSHRA.txt file
        with open(file_path, 'w') as f:
            f.write(contents)
        print("MUSHRA File Contents:")
        print(contents)

    def next_trial(self, app_instance):
        # Stop playing audio
        pygame.mixer.music.stop()
        # Save the scores to the corresponding trial file
        data_dir = os.path.join(os.getcwd(), "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        trial_scores_file = os.path.join(data_dir, f"MUSHRAPF{app_instance.current_trial}.txt")
        with open(trial_scores_file, 'w') as f:
            for button, file_used in app_instance.scores.items():
                f.write(f"{button} = {file_used}\n")
                # Write slider values to the file
                f.write(f"{button} = {getattr(app_instance, f'{button}_slider').get()}\n")
        # Reset slider values to 0 for A-E
        for button_text in ['A', 'B', 'C', 'D', 'E']:
            getattr(app_instance, f"{button_text}_slider").set(0)
        # Move to the next trial or end the test
        if app_instance.current_trial < 5:
            app_instance.current_trial += 1
            app_instance.trial_label.config(text=f"Trial {app_instance.current_trial} out of 5")
            # Reset player controls
            app_instance.loop_var.set(False)
            app_instance.audio_slider.set(0)
            # Reset available files for the next trial
            app_instance.available_files = list(range(1, 6))  # Reset available_files
            app_instance.scores = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}  # Reset scores
            # Randomly assign files to buttons for the next trial
            self.randomize_files(app_instance)
        else:
            self.end_screen(app_instance)

    def end_screen(self, app_instance):
        end_screen = tk.Toplevel()
        end_screen.title("End Screen")
        end_label = tk.Label(end_screen, text="Thank you for answering. Please proceed to the Method of Adjustment.")
        end_label.pack(pady=20)
        close_button = ttk.Button(end_screen, text="Close", command=end_screen.destroy)
        close_button.pack(pady=10)

    def randomize_files(self, app_instance):
        # Randomly assign files to A-E buttons for the current trial
        random.shuffle(app_instance.available_files)
        for button_text in ['A', 'B', 'C', 'D', 'E']:
            file_number = app_instance.available_files.pop(0)
            file_path = os.path.join(os.getcwd(), "eq", f"{file_number}.txt")
            app_instance.scores[button_text] = f"{file_number}.txt"
            print(f"Button {button_text} assigned file {file_path}")
