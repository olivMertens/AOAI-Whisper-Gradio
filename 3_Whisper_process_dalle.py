"""
3_Whisper_process_dalle.py

This script provides functionalities for processing audio files, translating audio language, generating text with GPT models, and creating images with DallE 2. It also includes a Gradio interface for user interaction.

Functions:
- translateAudioLanguage(text2Speech, paramVoice): Translates the provided text into speech in the specified language using Azure Speech SDK.
- processAudio(audio1, audio2, choiceParamWhisper, choiceImprove, systemPromptAudio, temperature, gptChosen): Processes the provided audio file(s) using the Whisper ASR model. It can optionally enhance the result with GPT models.
- countCharacter(input): Counts the number of characters in the provided input. Returns an error message if the character count exceeds 1000.
- updateEveryTextBox(inputProcess, outputProcess): Updates the output text box with the provided input text.
- processGpt(inputProcess, systemPrompt, temperature, gptChosen): Generates text using the selected GPT model based on the provided input text and system prompt.
- promptInsert(selectProcess): Generates a system prompt based on the selected process type.
- promptImageDef(promptImage): Generates an image using DallE 2 based on the provided prompt.

Gradio Interface:
- Tab 1: Allows users to record or upload an audio file and transcribe or translate it using the Whisper ASR model. Users can also choose to enhance the result with GPT models and provide a system prompt for the output.
- Tab 2: Allows users to generate text using the selected GPT model based on the provided input text and system prompt. Users can also choose to generate a JSON output with additional information.
- Tab 3: Allows users to generate an image using DallE 2 based on the provided prompt.

Extra Parameters:
- temperature: A slider for adjusting the creativity level of the GPT model.
- gptChosen: A dropdown for selecting the GPT model to use.

Please ensure that the necessary Python packages (Gradio, OpenAI-Whisper, OpenAI-GPT, and DallE-2) are installed and that the Azure endpoint and key details are correctly set as environment variables for the Azure functionalities.
"""
import gradio as gr, os
import openai, dotenv
from openai import AzureOpenAI
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv("azure.env")

# Setting Open Ai organization
openai.organization = os.getenv('OPENAI_ORGANIZATION')


class Azure:
    def __init__(self):
        self.api_base = None
        self.api_key = None
        self.api_version = None
        self.api_type = None
azure = Azure()

# Setting Azure OpenAI endpoint parameters
azure.openai_api_base = os.getenv('AZURE_OPENAI_API_BASE')
azure.openai_api_key = os.getenv('AZURE_OPENAI_API_KEY')     
azure.openai_api_version = os.getenv('AZURE_OPENAI_API_VERSION')
azure.openai_api_type = os.getenv('AZURE_OPENAI_API_TYPE')

# Settings Azure Speech & Whisper
azure.speech_endpoint = os.getenv('AZURE_SPEECH_ENDPOINT')
azure.whisper_deployment_id = os.getenv('AZURE_WHISPER_DEPLOYMENT_ID')
azure.whisper_model = os.getenv('AZURE_WHISPER_MODEL')
azure.whisper_key = os.getenv('AZURE_WHISPER_KEY')

#Settings for DallE

class Dalle:
    def __init__(self):
        self.api_key = None
        self.endpoint = None
dalle = Dalle()

dalle.api_key = os.getenv('AZURE_DALLE_API_KEY')
dalle.endpoint = os.getenv('AZURE_DALLE_ENDPOINT')

systemPromptAudio = ""


def processAudio(audio1,audio2, choiceParamWhisper, choiceImprove ,systemPromptAudio, temperature = 0, gptChosen = "gpt-35-turbo"):
    if audio1 is None and audio2 is None:
        return "No audio inputs were provided."
    elif audio1 is None:
        # Process only the second audio input
        audioOk = audio2
    elif audio2 is None:
        # Process only the first audio input
        audioOk = audio1
    else: 
        audioOk = audio1

    clientWhisper = AzureOpenAI(
        api_key = azure.whisper_key,
        azure_endpoint = azure.speech_endpoint,
        azure_deployment= azure.whisper_deployment_id,
        api_version= azure.openai_api_version
    )

    if choiceParamWhisper == "translate":
        with open(audioOk, "rb") as audio_file:
            whisperResult = clientWhisper.audio.translations.create(
                file=audio_file,
                model=azure.whisper_model,
                response_format="text",
                temperature=temperature
            )
    else:
        with open(audioOk, "rb") as audio_file:
            whisperResult = clientWhisper.audio.transcriptions.create(
                file=audio_file,
                model=azure.whisper_model,
                response_format="text",
                temperature=temperature
            )

    if(choiceImprove == "yes"):
        return processGpt(whisperResult,systemPromptAudio,temperature,gptChosen)
    else:
        return whisperResult

    
def countCharacter (input,dalleVersion = "dall-e-3"):
            
            numberCharacter = 4000
            if len(input) > numberCharacter:
                    return "Input is too long! Maximum length is "+numberCharacter+" characters."
            else:
        
             return input

def processGpt (inputProcess, systemPrompt, temperature = 0, gptChosen = "gpt-35-turbo"):

    clientGpt = AzureOpenAI(
            api_key=azure.openai_api_key,
            api_version=azure.openai_api_version,
            azure_deployment=gptChosen,  # i made my deployment id identical to  the model for accelerate and decrease the complexity ( so same var but could be different for you between deployment_id and model)
            azure_endpoint=azure.openai_api_base
    )

    answer = clientGpt.chat.completions.create(
        temperature=temperature,
        model=gptChosen,
        messages=[
                {"role": "system", "content": systemPrompt},
                {"role": "user", "content": inputProcess},
            ]
        )
 
    return answer.choices[0].message.content

def promptInsert (selectProcess):

    systemPrompt="You are a chatbot who have received text from an audio file, you have to describe what it's going on, you have to be precise and identify by a name each person ,you could give advice for the situation, resume and give the sentiment about it"
    
    if selectProcess == 1:
        systemPrompt += " You have also to give a json format readable by a computer where you have to give the keys : name, resume, sentiment , advice to help the situation and be sure that it's correctly closed at the end."
   
    elif selectProcess == 2:
        systemPrompt += " You have also to give a json format readable by a computer where you have to give the keys : name, resume, sentiment , advice to help the situation and be sure that it's correctly closed at the end."
        systemPrompt += " You have to create and give a prompt in order to creat an image based on the situation. The image will be sent by email to the person who has sent the audio file. It must be a photorealistic prompt and describe precisely the text"
    else:
        pass

    return systemPrompt

def promptImageDef (promptImage,dalleVersion,dalleSize,dalleQuality,dalleStyle):


    clientDallE = AzureOpenAI(
            api_key=dalle.api_key,
            azure_deployment=dalleVersion,  # i made my deployment id identical to  the model for accelerate and decrease the complexity ( so same var but could be different for you between deployment_id and model)
            azure_endpoint=dalle.endpoint,
            api_version=azure.openai_api_version
    )

    imageGen = clientDallE.images.generate(
        prompt=promptImage,
        size=dalleSize,
        n=1,
        model=dalleVersion,
        style=dalleStyle,
        quality=dalleQuality,
    )
    return imageGen.data[0].url
# Gradio interface
with gr.Blocks() as demo:

    with gr.Tab(label="Text2speech with whisper"):
        textResultAudio = gr.TextArea(lines=20, placeholder="result will be here after submit",label="Results from audio",show_copy_button=True)
        gr.Interface(
            processAudio, 
            [
                gr.Audio(sources="microphone", type="filepath", label="Record Audio", show_label=True,  show_download_button=True),
                gr.Audio(sources="upload", type="filepath", label="Upload Audio", show_label=True),
                gr.Radio(["transcribe", "translate"], ["Transcribe with same language", "translate in english"], label="Translate or Transcribe", show_label=True, value="transcribe"),
                gr.Radio(["no","yes"], label="improve the result with GPT model", show_label=True, value="no"),
                gr.Text(lines=1, label="Prompt system for the output", show_label=True, value="You are a helpful assistant for a call center and you have to describe quickly and give some observations about the situation"),
            ],
            textResultAudio,
            title="Demo App Whisper model( AOAI ) / Prompt engineering / DallE generation",
            description="Record your speech via microphone or upload an audio file and press the Submit button to transcribe it into text. Please, note that the size of the audio file should be less than 25 MB.",
            allow_flagging="never",
            article="Interface to whisper model /  Process outputs  /  DallE image generate"
        )
        
    with gr.Tab(label="Process Audio text by GPT"):
        with gr.Row():
            with gr.Column():

                text2ProcessGpt = gr.TextArea(placeholder="copy/paste the text for processing",label="Process with gpt",show_label=True, interactive=True)

                selectProcess = gr.Dropdown(
                ["Explain", "Explain with Json format output", "Explain with Json output and image prompt"], label="Process", info="You can choose the type of process or prompting the text from Tab audio with whisper", value="Explain", type="index", interactive=True)
                promptPlace= gr.TextArea(placeholder="Here is the prompt",label="Prompt for process request", show_label=True,interactive=True)
                
                buttonSpeech = gr.Button('Process the audio speech',variant="primary")
                gr.ClearButton([promptPlace,text2ProcessGpt],value="Clear Prompt")
            with gr.Column():
                text = gr.TextArea(autoscroll=False, placeholder="Result with your prompting/ask",label="Results from post processing",show_copy_button=True)
                
    with gr.Tab(label="Create Image - DallE"):
        with gr.Row():
            with gr.Column():
                promptImage= gr.Textbox(lines=20, placeholder="Your prompt for creating image",label="Prompt to DallE")
                promptImage.input(countCharacter,promptImage,promptImage)
                buttonProcessImage = gr.Button('Generate image from prompt',variant="primary")
            with gr.Column():
                imageGen = gr.Image(label="image generate by DallE")
    with gr.Tab(label="Generate audio with voice"):
        with gr.Row():
            with gr.Column():
                text2Speech = gr.Textbox(lines=4, placeholder="Your text for speech",label="Text to speech",show_label=True)
                paramVoice = gr.Radio(["en-US-AriaNeural","en-US-GuyNeural","en-US-JennyNeural","en-US-AriaNeural","PhoenixV2Neural"], label="Choose your Voice", show_label=True, value="en-US-AriaNeural")
                buttonVoice = gr.Button('Generate audio from text',variant="primary") 
            with gr.Column():
                audio = gr.Audio(label="audio generate by Azure speech") 
    with gr.Accordion("Extra params ",open=False):
        temperature= gr.Slider(minimum=0,maximum=1, step=0.1, value=0 ,label="0 deterministic, near or 1 random result")
        gptChosen = gr.Dropdown(["gpt-4","gpt-4-32k","gpt-35-turbo","gpt-35-turbo-16k"],["GPT4", "GTP4-32k", "GPT3.5TURBO","GPT3.5Turbo16K"],label="GPT model",value="gpt-4",type="value")
        dalleVersion = gr.Dropdown( ["dall-e-3"], label="DallE version", value="dall-e-3", type="value")
        dalleSize = gr.Dropdown(["1024x1024","1792x1024","1024x1792"],label="Size image",value="1024x1024",type="value")
        dalleStyle = gr.Dropdown(["natural","vivid"], label="DallE style", value="natural", type="value")
        dalleQuality = gr.Dropdown(["standard","hd"],label="DallE quality",value="standard",type="value")
        

        buttonSpeech.click(processGpt, inputs=[text2ProcessGpt,promptPlace,temperature,gptChosen], outputs=text)

        buttonProcessImage.click(promptImageDef,inputs=[promptImage,dalleVersion,dalleSize,dalleQuality,dalleStyle],outputs=imageGen)

        selectProcess.change(promptInsert, selectProcess, promptPlace)
if __name__ == "__main__":
    demo.launch()