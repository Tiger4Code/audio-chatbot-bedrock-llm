# Code snippets belong to www.youtube.com/@tiger4code channel

import json
import boto3
from datetime import datetime


def parse_transcript(response_uri):
    from urllib.parse import urlparse
    
    split_uri = response_uri.split('/')
    bucket_name = split_uri[3]
    object_key = "/".join(split_uri[4:])

    print(f" response_uri={response_uri}")    
    print(f" bucket_name= {bucket_name}")    
    print(f" object_key= {object_key}")    
    s3 = boto3.client('s3', region_name='us-east-1')
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    json_response = response['Body'].read().decode('utf-8')
    # Parse the JSON response and extract the "transcript"
    parsed_json = json.loads(json_response)
    transcribed_text = parsed_json['results']['transcripts'][0]['transcript']
    print(f" transcribed_text= {transcribed_text}")    

    return transcribed_text
    
    
def transcribe_audio(bucket, file_name, output_bucket_name, languageCode='en-US'):
    transcribe = boto3.client('transcribe', region_name='us-east-1')
    
    job_name = "audio2text-transcribe-job-" + datetime.now().strftime("%Y%m%d%H%M%S")
    job_uri = f"s3://{bucket}/{file_name}"

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode=languageCode, 
        OutputBucketName=output_bucket_name
    )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break

    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        response_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        print(f"response_uri: {response_uri}")
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        transcribed_text = parse_transcript(response_uri)
        return transcribed_text
        # return response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    else:
        return None

    # Replace 'your-job-name', 'your-bucket-name', and 'file_name' with appropriate values.


def lambda_handler(event, context):

    bucket = event['bucket']
    key = event['key']
    
    output_bucket_name = bucket
        
    transcribed_text = transcribe_audio(bucket=bucket, 
                                        file_name=key, 
                                        output_bucket_name=output_bucket_name, 
                                        languageCode='en-US')     

    return {
        'statusCode': 200,
        'text': transcribed_text, 
        'bucket':bucket
    }
