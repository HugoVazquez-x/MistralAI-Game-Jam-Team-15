# Code copied from https://elevenlabs.io/docs/cookbooks/text-to-speech/streaming

import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from typing import IO
from io import BytesIO
import yaml
import base64

client = ElevenLabs(
    api_key='', # bad practice but whatever
)

voices = {
    'politician1': 'ohZqJahxofk8dkPKmd9F',
    'politician2': 'v7sy7EHXxN3ToffFQfvr'
}



def read_audio_config(yaml_path: str) -> dict:
    try:
        with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at path '{yaml_path}' does not exist.")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")


def read_audio_file(audio_path: str):
        with open(audio_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
            return audio_base64


def text_to_speech_file(text: str, voice_id: str, stability=0.5, similarity=1.0, style=0.3, base_path='audio_store') -> str:
    """voice: politician1 or politician2"""
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id=voice_id, # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5", # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=1.0,
            style=0.3,
            use_speaker_boost=True,
        ),
    )

    
    save_file_path = os.path.join(base_path, f"{uuid.uuid4()}.mp3")

    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: audio file successfully saved !")

    return save_file_path




def text_to_speech_stream(text: str, voice: str, stability=0.5, similarity=1.0, style=0.3) -> IO[bytes]:
    """voice: politician1 or politician2"""
    # Perform the text-to-speech conversion
    response = client.text_to_speech.convert(
        voice_id=voices[voice], # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Create a BytesIO object to hold the audio data in memory
    audio_stream = BytesIO()

    # Write each chunk of audio data to the stream
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    # Reset stream position to the beginning
    audio_stream.seek(0)

    # Return the stream for further use
    return audio_stream




