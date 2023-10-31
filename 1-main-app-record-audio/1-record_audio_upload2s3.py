# Code snippets belong to www.youtube.com/@tiger4code channel

import lib.apigateway_functions as APIGateway_helper
import pyaudio
import lib.helper as Helper
import time 
# Constants for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5  # Adjust this to the desired recording duration

# S3 storage 
BUCKET_NAME = "REPLACE-WITH-YOUR-BUCKET-NAME"
OBJECT_PREFIX_KEY = "recording/"


print("1) Recording... Speak now!")
filename, audio_file_path = Helper.record_question_convert_wav(format=FORMAT, 
                                                                    channels=CHANNELS, 
                                                                    frame_rate=RATE, 
                                                                    chunk=CHUNK, 
                                                                    record_seconds=RECORD_SECONDS)

print("2) Upload recording to S3 ...")
object_name = f"{OBJECT_PREFIX_KEY}{filename}"
Helper.upload_audio_to_s3(file_path=audio_file_path, bucket_name=BUCKET_NAME, object_name=object_name)

print("3) Play recording (Question):")
Helper.play_wav(file_path=audio_file_path)

print("Call API Gateway to get the answer")
# Start the timer before the call
start_time = time.time()
apigateway_status_code, apigateway_response = APIGateway_helper.call_api_gateway(bucket=BUCKET_NAME, object_key=object_name)# payload_file_path='payload.json')
# End the timer after the call
end_time = time.time()
# Calculate the difference in seconds
duration_seconds = end_time - start_time
total_minutes, remaining_seconds = Helper.calculate_minutes_seconds(duration_seconds)
if apigateway_status_code == 200: 
    answer_bucket_name, answer_object_name = APIGateway_helper.process_api_gateway_response(apigateway_response)
    print(f"bucket={answer_bucket_name}, key={answer_object_name}")

    print("4) Download Answer ...")
    answer_audio_path = 'polly-audio/answer.mp3'
    local_path = Helper.download_from_s3(bucket_name=answer_bucket_name, 
                            object_name=answer_object_name, 
                            local_directory='polly-audio')
    print("5) Convert to WAV ...")
    answer_wav_file_path = Helper.convert_mp3_to_wav(mp3_file_path=local_path, CHANNELS=CHANNELS, FRAME_RATE=RATE)
    print("6) Play Answer ...")
    Helper.play_wav(file_path=answer_wav_file_path)
    print(" ---------------------- The End! --------------------")
else: 
    print("Ops, Something went wrong when calling the API, let me check ...")

print(" ---------------------- Time Consumed to answer the question  --------------------")
print(f"minutes={total_minutes}, seconds={remaining_seconds}")
print(" ---------------------------------------------------------------------------------")

