import whisper_at as whisper
from jiwer import wer
import argparse
import os
import string

# Function to preprocess text: remove punctuation and convert to lowercase
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    return text

# Function to calculate Word Accuracy Rate (WAR)
def calculate_war(reference_file, audio_file):
    # Load the Whisper model
    # model = whisper.load_model("large-v1")
    model = whisper.load_model("small.en")

    # Transcribe the audio file
    audio_tagging_time_resolution = 10
    result = model.transcribe(audio_file, at_time_res=audio_tagging_time_resolution)

    # Get the transcribed text
    transcribed_text = result["text"]
    print("ASR Results:", transcribed_text)

    # Load the reference transcription from the text file
    with open(reference_file, 'r') as file:
        reference_text = file.read().strip()

    # Preprocess both texts
    transcribed_text = preprocess_text(transcribed_text)
    reference_text = preprocess_text(reference_text)

    # Calculate the Word Error Rate (WER)
    error_rate = wer(reference_text, transcribed_text)

    # Calculate Word Accuracy Rate (WAR)
    war = (1 - error_rate) * 100
    return war

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Calculate Word Accuracy Rate (WAR) using Whisper model.")
    parser.add_argument('reference_file', type=str, help='Path to the reference transcription text file')
    parser.add_argument('audio_file', type=str, help='Path to the audio file to be transcribed')
    
    args = parser.parse_args()
    
    # Ensure files exist
    if os.path.exists(args.reference_file) and os.path.exists(args.audio_file):
        # Calculate WAR
        war = calculate_war(args.reference_file, args.audio_file)
        print(f"Word Accuracy Rate: {war:.2f}%")
    else:
        print("Reference file or audio file not found.")

if __name__ == "__main__":
    main()
