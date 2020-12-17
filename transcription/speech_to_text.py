# from googletrans import Translator
# import speech_recognition as sr
# from gtts import gTTS 
from playsound import playsound
from os import path
import wave
import speech_recognition as sr
from ibm_watson import SpeechToTextV1
import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# playsound('./Audio/sample1.wav')
# IBM Speech Recognition - Speech to Text
def recognize(filename):
    with open(f'./uploads/{filename}', 'rb') as audio_file:
        speech_recognition_results = service.recognize(audio=audio_file, content_type='audio/wav').get_result()
    return speech_recognition_results

authenticator = IAMAuthenticator('YOURKEY')
service = SpeechToTextV1(
   authenticator=authenticator
)
service.set_service_url('https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/6e83f6c6-6e54-4baf-b77c-8f2245b06a01')
# recognize('sample2.wav')
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "./Audio/sample1.wav")
# print(speech_recognition_results)
