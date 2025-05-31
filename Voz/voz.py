import speech_recognition as sr

recognizer = sr.Recognizer()

while True:
    try:
        with sr.Microphone() as source:
            print("Diga algo...")
            recognizer.adjust_for_ambient_noise(source, duration=0.1)
            audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
        text = text.lower()
        print(f"Você disse: {text}")
    except sr.UnknownValueError:
        print("Não consegui entender o áudio")
    except sr.RequestError as e:
        print(f"Erro na solicitação: {e}")
    except KeyboardInterrupt:
        print("Saindo...")
        break
    except Exception as e:
        print(f"Ocorreu um erro: {e}")  