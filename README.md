# Jump-start Python templates to demo Whisper in the Gradio-powered Web apps
Whisper models allow you to transcribe and translate audio files, using their speech-to-text capabilities.

In this repo I'll demo how to utilise Whisper offline or consume it through Azure endpoints (either from [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/overview) or [Azure AI Speech](https://learn.microsoft.com/en-GB/azure/ai-services/speech-service/overview) resources).

Each option from the table of contents below is wrapped into a functional Web interface, powered by [Gradio](https://www.gradio.app/) platform.

## Table of contents:
- [Option 0 - Access to Whisper models in offline mode](https://github.com/LazaUK/AOAI-Whisper-Gradio/blob/main#option-0---access-to-whisper-models-in-offline-mode)
- [Option 1 - Access to Whisper models via Azure OpenAI endpoint](https://github.com/LazaUK/AOAI-Whisper-Gradio/tree/main#option-1---access-to-whisper-models-via-azure-openai-endpoint)
- [Option 2 - Access to Whisper models via Azure AI Speech endpoint](https://github.com/LazaUK/AOAI-Whisper-Gradio/blob/main#option-2---access-to-whisper-models-via-azure-ai-speech-endpoint)

## Option 0 - Access to Whisper models in offline mode
Whisper model can be consumed offline. As a trade-off, you may notice difference in its performance in comparison to an Azure based deployment. To instantiate Web app with offline Whisper functionality, please follow these steps:
1. Install gradio Python library. This will allow you to define and instantiate a Web app, that will run locally as a Web service.
```
pip install --upgrade gradio
```
2. 

## Option 1 - Access to Whisper models via Azure OpenAI endpoint

## Option 2 - Access to Whisper models via Azure AI Speech endpoint
