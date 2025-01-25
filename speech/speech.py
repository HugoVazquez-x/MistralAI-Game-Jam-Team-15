# Code copied from https://elevenlabs.io/docs/cookbooks/text-to-speech/streaming

import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from typing import IO
from io import BytesIO

client = ElevenLabs(
    api_key='',
)

voices = {
    'politician1': 'ohZqJahxofk8dkPKmd9F',
    'politician2': 'v7sy7EHXxN3ToffFQfvr'
}


def text_to_speech_file(text: str, voice: str, stability=0.5, similarity=1.0, style=0.3) -> str:
    """voice: politician1 or politician2"""
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id=voices[voice], # Adam pre-made voice
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

    # uncomment the line below to play the audio back
    # play(response)

    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
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




