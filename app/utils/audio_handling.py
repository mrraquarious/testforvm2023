import os
import openai
import wave
import shutil
import contextlib
from moviepy.editor import *
import librosa
import soundfile as sf
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def convert_audio_to_wav(input_file, output_file):
    print("Covnersion begins")
    # Extract the extension from the input file
    _, input_ext = os.path.splitext(input_file)

    # Check if the input file extension is valid
    valid_extensions = [".mp4", ".mp3", ".wav", ".mpga", ".webm"]
    if input_ext.lower() not in valid_extensions:
        raise ValueError(f"Invalid input file format. Supported formats are: {', '.join(valid_extensions)}")

    if input_ext.lower() == ".wav":
        # If the input file is already a WAV file, just copy it to the output file
        shutil.copyfile(input_file, output_file)
    else:
        # Load the audio file
        y, sr = librosa.load(input_file, sr=None)

        # Resample the audio to a lower sample rate
        target_sample_rate = 10000
        y_resampled = librosa.resample(y, orig_sr=sr, target_sr=target_sample_rate)

        # Save the resampled audio as a WAV file
        sf.write(output_file, y_resampled, target_sample_rate, subtype='PCM_16')
    print("Conversion succeed")


def slice_audio_file(audio_file, max_size):
    with contextlib.closing(wave.open(audio_file, "rb")) as audio:
        total_frames = audio.getnframes()
        sample_width = audio.getsampwidth()
        sample_rate = audio.getframerate()
        num_channels = audio.getnchannels()

        bytes_per_frame = sample_width * num_channels
        max_frames = (max_size // bytes_per_frame)

        sliced_audio_files = []
        for i in range(0, total_frames, max_frames):
            sliced_file_name = f"sliced_{i}_{'_'.join(audio_file.split('/'))}"
            with wave.open(sliced_file_name, "wb") as sliced_audio:
                sliced_audio.setnchannels(num_channels)
                sliced_audio.setsampwidth(sample_width)
                sliced_audio.setframerate(sample_rate)

                frames_to_write = min(max_frames, total_frames - i)
                sliced_audio.writeframes(audio.readframes(frames_to_write))

            sliced_audio_files.append(sliced_file_name)

    return sliced_audio_files

def transcribe_audio_file(audio_file):
    with open(audio_file, "rb") as audio:
        print("Sending to openai whisper .....")
        transcript_response = openai.Audio.transcribe("whisper-1", audio)
        print("Received from openai whispter .....")
    return transcript_response["text"]

def combine_transcripts(transcripts):
    return " ".join(transcripts)




def load_audio(temp_file,temp_wav_file,max_size = 20 * 1024 * 1024):
    print("working fine")

    convert_audio_to_wav(temp_file, temp_wav_file)

    # return "this is a test"

    if os.path.getsize(temp_wav_file) > max_size:
        sliced_audio_files = slice_audio_file(temp_wav_file, max_size)
        transcripts = []

        for audio_file in sliced_audio_files:
            transcript = transcribe_audio_file(audio_file)
            transcripts.append(transcript)
            os.remove(audio_file)  # Remove the sliced audio file after transcribing

        combined_transcript = combine_transcripts(transcripts)
    else:
        combined_transcript = transcribe_audio_file(temp_wav_file)
    os.remove(temp_wav_file)
    return combined_transcript


### DEBUG ONLY ###
# temp_file = "training/uploads/single_test_audio.wav"

# root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# temp_wav_file = os.path.join(root_dir, "test_audio.wav")

# max_size = 20 * 1024 * 1024  # 24 MB

# print(load_audio(temp_file,temp_wav_file,max_size))
