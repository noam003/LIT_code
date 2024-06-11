# Noa M
# Local file for going from flac files (in the Librispeech database) to wav
from pydub import AudioSegment
import os

# Path to the directory containing the FLAC files
full_path = "/Users/noamargolin/Downloads/LibriSpeech/dev-clean/3853/163249"

# Path to the new folder on the Desktop
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
new_folder_name = '3853'
new_folder_path = os.path.join(desktop_path, new_folder_name)
os.makedirs(new_folder_path, exist_ok=True)

# Iterate over the files in the directory
for file_name in os.listdir(full_path):
    if file_name.endswith(".flac"):
        # Construct the full path to the FLAC file
        audio_path = os.path.join(full_path, file_name)

        # Extract the name for the WAV file
        name_wav = file_name[-9:-5] + ".wav"

        # Construct the full path for the new WAV file
        new_file_path = os.path.join(new_folder_path, name_wav)

        # Convert the FLAC file to WAV and save it
        audio = AudioSegment.from_file(audio_path, format="flac")
        audio = audio.set_frame_rate(8000)
        audio.export(new_file_path, format="wav")

        print(f"Converted {file_name} to {new_file_path}")

print("All files have been processed and saved.")