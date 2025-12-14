import asyncio
from unittest import result
import gradium
import os 
import struct
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GRADIUM_API_KEY")

client = gradium.client.GradiumClient(api_key=api_key)

SAMPLE_RATE = 48000
async def test_tts(client = client,text: str = "Hello, world! This is a test of the Gradium Text-to-Speech API.", voice: str = "YTpq7expH9539ERJ", output_file : str = "output.wav"):
    result = await client.tts(
        setup={
            "model_name": "default", 
            "voice_id": voice,
            "output_format": "wav"
        },
        text=text
    )
    with open(output_file, "wb") as f:
        f.write(result.raw_data)



async def test_tts_stream(client,text_to_speak: str = "Hello, world! This is a test of the Gradium Text-to-Speech streaming API.", voice: str = "LFZvm12tW_z0xfGo", output_file : str = "output_stream.pcm" ):
    

    print(f"Requesting TTS stream for: '{text_to_speak}'")
    
    gradium_stream = await client.tts_stream(
        setup={
            "model_name": "default",
            "voice_id": voice,
            "output_format": "pcm"
        },
        text=text_to_speak)
    async for audio_chunk in gradium_stream.iter_chunks():
        print(f"Received audio chunk of size: {len(audio_chunk)} bytes")
        # Here you could write the chunk to a file or process it further
    

if __name__ == "__main__":
    # asyncio.run(test_tts_stream())
    asyncio.run(test_tts())
