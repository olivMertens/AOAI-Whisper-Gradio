"""
This script is a demo app for the Whisper model through Azure AI Speech endpoint.
Source code is taken from: https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/batch/python/python-client/main.py
"""

import gradio as gr
import sys, requests, time,os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
load_dotenv("azure.env")


class Azure:
    def __init__(self):
        self.speech_endpoint = None
        self.speech_key = None
        self.speech_region = None
azure = Azure()
# Setting Azure Speech parameters
azure.speech_endpoint = os.getenv('AZURE_SPEECH_ENDPOINT')
azure.speech_key = os.getenv('AZURE_SPEECH_KEY')
azure.speech_region = os.getenv('AZURE_SPEECH_REGION')




def translateAudioLanguage (text2Speech,paramVoice):
        speech_config = speechsdk.SpeechConfig(subscription=azure.speech_key, region=azure.speech_region)

        speech_config.speech_synthesis_voice_name = paramVoice
                # use the default speaker as audio output.
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        return speech_synthesizer.speak_text_async(text2Speech).get()

def transcribe_from_single_blob(uri, properties):
    """
    Transcribe a single audio file located at `uri` using the settings specified in `properties`
    using the base model for the specified locale.
    """
    transcription_definition = swagger_client.Transcription(
        display_name=NAME,
        description=DESCRIPTION,
        locale=LOCALE,
        content_urls=[uri],
        properties=properties
    )

    return transcription_definition


def transcribe_with_custom_model(client, uri, properties):
    """
    Transcribe a single audio file located at `uri` using the settings specified in `properties`
    using the base model for the specified locale.
    """
    # Model information (ADAPTED_ACOUSTIC_ID and ADAPTED_LANGUAGE_ID) must be set above.
    if MODEL_REFERENCE is None:
        logging.error("Custom model ids must be set when using custom models")
        sys.exit()

    model = {'self': f'{client.configuration.host}/models/{MODEL_REFERENCE}'}

    transcription_definition = swagger_client.Transcription(
        display_name=NAME,
        description=DESCRIPTION,
        locale=LOCALE,
        content_urls=[uri],
        model=model,
        properties=properties
    )

    return transcription_definition

def transcribe(audio):

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="en-US")
    result = speech_recognizer.recognize_once_async().get()
    print(result.text)

demo = gr.Interface(
    transcribe, gr.Audio(source="microphone", type="filepath", label="Audio Recording"), "textbox",
    title="Demo App 2: Whisper model through Azure AI Speech endpoint",
    description="Record your speech via microphone and press the Submit button to transcribe it into text. Please, note that the size of the audio file should be less than 1 GB."
)

if __name__ == "__main__":
    demo.launch()