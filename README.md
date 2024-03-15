# MUSHRA-headphone-virtualizer
A listening test software that allows double-blind rapid comparisons between virtualized headphone frequency responses.

## Setup
The MUSHRA-headphone-virtualizer requires installing Python 3.11.x.
First, you must install the tkinter module, the openpyxl module, and the pygame module, so in Command Prompt, type:
```
pip install tk openpyxl pygame
```
Afterwards, run the main python file (main.py)
## Instructions of usage:
1) Import MUSHRA.txt onto EqualizerAPO on the config folder. You may use the contents of Preference.txt from MOA-test as a placeholder.
```
Preamp: -10 dB
Filter 1: ON LSC Fc 112 Hz Gain 0 dB Q 0.350
Filter 2: ON HSC Fc 3550 Hz Gain 0 dB Q 0.350
Filter 3: ON LSC Fc 105 Hz Gain 0.00 dB Q 0.770
Filter 4: ON HSC Fc 2500 Hz Gain 0 dB Q 0.390
Filter 5: ON PK Fc 2800 Hz Gain 0 dB Q 1.800
Filter 6: ON LSC Fc 50 Hz Gain 0.00 dB Q 0.500
```
2) Create eq/ folder in the same directory with different EQ for the headphones with the title "1.txt" to "5.txt".
3) Music files has to be placed inside the "music" folder, titled "1.wav" to "5.wav"
