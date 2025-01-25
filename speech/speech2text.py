import speech_recognition as sr
import requests

HF_API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
# HF_API_URL = "https://api-inference.huggingface.co/models/facebook/s2t-small-librispeech-asr"
HF_API_TOKEN = ""  # Replace with your Hugging Face API token

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def microphone_to_text():
    # Initialize the speech recognition engine
    recognizer = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening... Please speak now.")

        try:
            audio = recognizer.listen(source, timeout=10)  # Timeout after 10 seconds
            print("Processing your speech...")
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
            return

    try:
        audio_data = audio.get_wav_data()
    except Exception as e:
        print(f"Error processing audio: {e}")
        return

    print("Sending audio to hf for transcription...")
    try:
        response = requests.post(HF_API_URL, headers=headers, data=audio_data)
        response.raise_for_status()  # Raise an exception for HTTP errors

        transcription = response.json()
        print(f"Transcription: {transcription.get('text', 'No text found')}")
    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    microphone_to_text()
