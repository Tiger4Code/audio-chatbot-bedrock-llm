# Code snippets belong to www.youtube.com/@tiger4code channel

import boto3
from pydub import AudioSegment
import pyaudio
import wave


# Constants for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5  # Adjust this to the desired recording duration

def record_question_convert_wav(format=FORMAT, 
                                channels=CHANNELS, 
                                frame_rate=RATE, 
                                chunk=CHUNK, 
                                record_seconds=RECORD_SECONDS):
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    # Start recording

    stream = audio.open(format=format, channels=channels,
                        rate=frame_rate, input=True,
                        frames_per_buffer=chunk)
    frames = []

    for _ in range(0, int(frame_rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop recording
    print("Recording stopped.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a WAV file
    filename = gen_filename()
    audio_file_path = f"recording/{filename}"
    with wave.open(audio_file_path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(frame_rate)
        wf.writeframes(b''.join(frames))

    return filename, audio_file_path


def play_wav(file_path):
    print(f"Currently playing {file_path}")
    # Set chunk size of 1024 samples per data frame
    chunk = 1024  
    # Open the sound file 
    wf = wave.open(file_path, 'rb')
    # Create an interface to PortAudio
    p = pyaudio.PyAudio()
    # Open a .wav format music file
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
    # Read data in chunks
    data = wf.readframes(chunk)
    # Play the sound by writing the audio data to the stream
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    # Close and terminate the stream
    stream.close()
    p.terminate()


# Replace 'file_path' with the path to your local audio file and replace 'bucket_name' and 'object_name' with your S3 bucket and object names respectively.
def gen_filename(extension='wav'):
    import datetime

    # Get the current date and time
    current_time = datetime.datetime.now()
    # Format the timestamp as a string
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    # Create a file name with the timestamp
    file_name = f"audio_{timestamp}.{extension}"  # Adjust the prefix and file extension as needed
    # print("Generated file name:", file_name)
    return file_name


def convert_mp3_to_wav(mp3_file_path, CHANNELS=2, FRAME_RATE=44100):
    try:
        # file_name = mp3_file_path.rsplit('.', 1)[0]
        # wav_file_path = f"{file_name}.wav"
        wav_file_path = mp3_file_path.replace(".mp3", ".wav")
        sound = AudioSegment.from_mp3(mp3_file_path)
        sound = sound.set_channels(CHANNELS)  # Set the number of channels to match the recorded audio
        sound = sound.set_frame_rate(FRAME_RATE)  # Set the frame rate to match the recorded audio
        sound.export(wav_file_path, format="wav")
        return wav_file_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def upload_audio_to_s3(file_path, bucket_name, object_name):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File uploaded successfully to {bucket_name}/{object_name}")
    except FileNotFoundError:
        print(f"The file {file_path} was not found")

# return local_path 
def download_from_s3(bucket_name, object_name, local_directory='polly-audio'):
    import os
    s3 = boto3.client('s3')
    try:
        # Ensure the local directory exists
        os.makedirs(local_directory, exist_ok=True)

        # Extract the file name from the object_name
        file_name = object_name.split('/')[-1]

        # Define the local file path
        local_path = os.path.join(local_directory, file_name)

        # Download the file from S3 to the local directory with the same name
        s3.download_file(bucket_name, object_name, local_path)
        print(f"File downloaded to {local_path}")
        return local_path
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'bucket_name' and 'object_name' with your actual S3 bucket name and file name
# download_from_s3('bucket_name', 'object_name')


# Replace 'bucket_name' and 'object_name' with your actual S3 bucket name and file name
# load_and_play_audio_from_s3('bucket_name', 'object_name')

# Convert the duration to minutes and seconds
def calculate_minutes_seconds(total_seconds):
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return minutes, seconds