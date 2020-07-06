import speech_recognition as sr

from gtts import gTTS
from googletrans import Translator
from playsound import playsound


def SpeechToText():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source)
        print("Diga alguma coisa:")
        audio = microfone.listen(source)

        try:
            frase = microfone.recognize_google(audio, language='pt-BR')
            print("Você disse: " + frase)
            return frase

        except sr.UnkownValueError:
            #cria_audio("Não entendi")
            return False


def TextToSpeech(text, lang='pt-br'):
    tts = gTTS(text, lang=lang)
    tts.save('audios/text.mp3')
    playsound('audios/text.mp3')
