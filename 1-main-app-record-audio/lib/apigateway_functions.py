import requests
import json

def call_api_gateway(bucket, object_key): #, payload_file_path='payload.json'):
    # Replace the url below with the url from your API Gateway
    url = 'https://STRING.execute-api.REAGION.amazonaws.com/STAGE-NAME/RESOURCE-NAME'  # Replace with your API Gateway endpoint URL

    # Create the JSON object
    payload = {
        "bucket": bucket,
        "key": object_key
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print("API call successful.")
        print("Response:", response.json())  # If the response is expected to be in JSON format.
        return response.status_code, response.json()
    else:
        print("API call failed with status code:", response.status_code)
        print("Response:", response.text)  # Print the response content for further inspection.
        return response.status_code, response.text

# return bucket and key name
def process_api_gateway_response(apigateway_response):
    # Load the 'body' from the JSON response
    body = json.loads(apigateway_response['body'])

    # Extract the bucket and key names
    bucket = body['bucket']
    key = body['key']

    return bucket, key