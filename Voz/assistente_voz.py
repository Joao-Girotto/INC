import pyttsx3
import speech_recognition as sr
from datetime import datetime
import webbrowser

engine = pyttsx3.init()

for voz in engine.getProperty('voices'):
    if 'portuguese' in voz.name.lower() or 'brazil' in voz.name.lower() or 'pt' in voz.id.lower():
        engine.setProperty('voice', voz.id)
        break

engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def falar(texto):
    engine.say(texto)
    engine.runAndWait()

def ouvir():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga um comando.")
        audio = recognizer.listen(source)
    try:
        comando = recognizer.recognize_google(audio, language='pt-BR')
        return comando.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def main():
    while True:
        comando = ouvir()
        if 'que horas são' in comando:
            hora_atual = datetime.now().strftime("%H:%M")
            falar(f"Agora são {hora_atual}")
        elif 'abrir navegador' in comando:
            falar("Abrindo o navegador.")
            webbrowser.get().open('https://www.google.com')  # Abre no navegador padrão
        elif 'sair' in comando:
            falar("Saindo do programa.")
            break

if __name__ == "__main__":
    main()
