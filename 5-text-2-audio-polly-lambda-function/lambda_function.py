import boto3
"""
voice_id
Joanna, Matthew, Salli, Ivy, Kendra, Kimberly, Joey, Justin, Raveena, Nicole 
"""
def gen_filename():
    import datetime

    # Get the current date and time
    current_time = datetime.datetime.now()

    # Format the timestamp as a string
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    # Create a file name with the timestamp
    file_name = f"polly_audio_{timestamp}.mp3"  # Adjust the prefix and file extension as needed

    # print("Generated file name:", file_name)
    return file_name
    
def lambda_handler(event, context):
    text = event['text']
    voice_id = event.get('voice_id', 'Joanna')  # Default voice_id is Joanna
    s3_bucket = event['bucket']  # Replace with your S3 bucket name
    file_name = gen_filename()
    s3_key = f"polly-audio/{file_name}" 
    
    polly = boto3.client('polly')
    s3 = boto3.client('s3')

    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        # OutputFormat="pcm",
        VoiceId=voice_id
    )

    s3.put_object(
        Bucket=s3_bucket,
        Key=s3_key,
        Body=response['AudioStream'].read()
    )

    return {
        'statusCode': 200,
        'bucket': s3_bucket, 
        'key': s3_key, 
    }
