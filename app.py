import speech_recognition as sr
import RPi.GPIO as GPIO
import time, sys
from gtts import gTTS  # Additionally added speak function
import subprocess, tempfile, os

MIC_INDEX   = 3    
SAMPLE_RATE = 44100

GPIO.setwarnings(False)      
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)

r = sr.Recognizer()

def speak(msg: str, *, lang="en", tld="com.au"):
    mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    gTTS(msg, lang=lang, tld=tld).save(mp3)
    subprocess.run(["mpg123", "-q", mp3])
    os.remove(mp3)

try:
    while True:
        try:
            with sr.Microphone(device_index=MIC_INDEX,
                               sample_rate=SAMPLE_RATE) as source:
                print("\nAdjusting for ambient noise... Please wait.")
                r.adjust_for_ambient_noise(source, duration=1)
                print("Now speak!")

                # optionally limit how long we wait/listen
                audio = r.listen(source, timeout=5, phrase_time_limit=4)

            print("\nRecognizing...")
            text = r.recognize_google(audio)
            print("You said:", text)

            if "turn on" in text.lower():
                print("Turn on LED")
                speak("Turn on LED")
                GPIO.output(13, GPIO.HIGH)

            elif "turn off" in text.lower():
                print("Turn off LED")
                speak("Turn off LED")
                GPIO.output(13, GPIO.LOW)                      

        except (sr.UnknownValueError,
                sr.RequestError,
                sr.WaitTimeoutError):                
            print("Your voice cannot be recognized. Try again")                
            continue
            
except KeyboardInterrupt:
    GPIO.cleanup()              
    sys.exit(0)
