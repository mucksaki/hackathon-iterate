import requests
import os 
import time
from dotenv import load_dotenv
import json
import ast

load_dotenv()
api_key = os.environ['PYANNOTE_API_KEY']

def upload_wav_to_pyannote(file_path: str, object_key: str) -> str: 
    # Define your media object key
    # object_key = "my-meeting-recording"  # Replace with your desired object-key

    # Create the pre-signed PUT URL.
    # api_key = "YOUR_API_KEY"  # In production, use environment variables: os.getenv("PYANNOTE_API_KEY")
    response = requests.post(
        "https://api.pyannote.ai/v1/media/input",
        json={"url": f"media://{object_key}"},
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    response.raise_for_status()
    data = response.json()
    presigned_url = data["url"]

    # Upload local file to the pre-signed URL.
    # input_path = '/home/yosh/audio_ml/sample_fr_hibiki_crepes.mp3'
    # print("Uploading {0} to {1}".format(file_path, presigned_url))

    with open(file_path, "rb") as input_file:
        # Upload your local audio file.
        requests.put(presigned_url, data=input_file)
    
    return object_key

def get_text(object_key: str) -> str:
    body = {
    "url" : f"media://{object_key}",
    "transcription": True,
    }

    url = "https://api.pyannote.ai/v1/diarize"
    headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
    }

    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    job_id = response.json()['jobId']
    headers = {"Authorization": f"Bearer {api_key}"}

    while True:
        response = requests.get(
            f"https://api.pyannote.ai/v1/jobs/{job_id}", headers=headers
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        data = response.json()
        status = data["status"]

        if status in ["succeeded", "failed", "canceled"]:
            if status == "succeeded":
                print("Job completed successfully!")
                # print(data["output"])
            else:
                print(f"Job {status}")
            break

        print(f"Job status: {status}, waiting...")
        time.sleep(5)  # Wait 10 seconds before polling again
    
    # print('-'*30)
    # print(f'data {data.keys()}')
    # print('finished while')
    json_data = parse_conv(data)
    return json_data

def parse_conv(data: dict):
    turns = data['output']['turnLevelTranscription']
    conv = []
    for turn in turns:
        text = turn['text']
        speaker = turn['speaker']
        # If the last entry has the same speaker, merge the text
        if conv and speaker in conv[-1]:
            conv[-1][speaker] += " " + text
        else:
            # Otherwise, add a new entry
            conv.append({speaker: text})
        # break

    json_data = json.dumps(conv, indent=2, ensure_ascii=False)
    return json_data


if __name__ == '__main__':
    # to be defined
    file_path = 'backend/src/audios/sample_13-11-14-45.wav'
    object_key = 'first-meeting'
    print('upload start ...')
    object_key = upload_wav_to_pyannote(file_path=file_path, object_key=object_key)
    print('upload finished')
    print('output start...')
    output = get_text(object_key=object_key)
    print(f'output: \n {output}')
