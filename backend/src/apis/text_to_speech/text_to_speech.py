import asyncio
import gradium
import os 
import struct
from dotenv import load_dotenv
import pyaudio
load_dotenv()
api_key = os.getenv("GRADIUM_API_KEY")

print(f"Loaded API Key: {api_key}")

SAMPLE_RATE = 48000


async def test_tts_stream():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=SAMPLE_RATE,
                    output=True)
    print("PyAudio stream opened.")
    
    client = gradium.client.GradiumClient(api_key=api_key)

    text_to_speak = "This is a longer text that will be streamed. We are testing the real-time playback capabilities using the Gradium Text-to-Speech streaming API and PyAudio.This is a longer text that will be streamed. We are testing the real-time playback capabilities using the Gradium Text-to-Speech streaming API and PyAudio.This is a longer text that will be streamed. We are testing the real-time playback capabilities using the Gradium Text-to-Speech streaming API and PyAudio.This is a longer text that will be streamed. We are testing the real-time playback capabilities using the Gradium Text-to-Speech streaming API and PyAudio.This is a longer text that will be streamed. We are testing the real-time playback capabilities using the Gradium Text-to-Speech streaming API and PyAudio.This is a longer text that will be streamed. We are testing the real-time playback capabilities using the Gradium Text-to-Speech streaming API and PyAudio.This is a longer text that will be streamed. We are testing the real-time playback capabilities using the Gradium Text-to-Speech streaming API and PyAudio.This is a longer text that will be streamed. We are testing the real-time playback capabilities using the Gradium Text-to-Speech streaming API and PyAudio.This is a longer text that will be streamed. We are testing the real-time playback capabilities using the Gradium Text-to-Speech streaming API and PyAudio.This is a longer text that will be streamed. We are testing the real-time playback capabilities using the Gradium Text-to-Speech streaming API and PyAudio.This is a longer text that will be streamed. We are testing the real-time playback capabilities using the Gradium Text-to-Speech streaming API and PyAudio."
    print(f"Requesting TTS stream for: '{text_to_speak}'")
    try:
        gradium_stream = await client.tts_stream(
            setup={
                "model_name": "default",
                "voice_id": "LFZvm12tW_z0xfGo",
                "output_format": "pcm"
            },
            text=text_to_speak)
        total_bytes = 0
        async for audio_chunk in gradium_stream.iter_bytes():
            # The streaming iterable is gradium_stream, not the PyAudio 'stream' object
            
            if audio_chunk:
                print(f"Received {len(audio_chunk)} bytes of audio.")
                # Write the received audio chunk to the PyAudio output stream
                stream.write(audio_chunk)
                total_bytes += len(audio_chunk)
        
        print(f"\nFinished receiving stream. Total bytes received: {total_bytes}")
    except Exception as e:
        print(f"Error initiating TTS stream: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("PyAudio stream closed.")

if __name__ == "__main__":
    asyncio.run(test_tts_stream())
