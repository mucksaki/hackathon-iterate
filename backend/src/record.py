import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 5  # Duration of recording

print("Recording...")
audio = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
write("output.wav", fs, audio)  # Save as WAV file
print("Saved as output.wav")

def record(output_name: str) -> None:
    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording

    print("Recording...")
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(f"{output_name}.wav", fs, audio)  # Save as WAV file
    print(f"Saved as {output_name}.wav")
