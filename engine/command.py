import datetime
import pyttsx3
import speech_recognition as sr
import eel
import time


def speak(text):
   text = str(text)
   engine = pyttsx3.init('sapi5')
   voices = engine.getProperty('voices')
   engine.setProperty('voice', voices[0].id)
   engine.setProperty('rate', 174)
   eel.DisplayMessage(text)
   engine.say(text)
   eel.receiverText(text)
   engine.runAndWait()


def takecommand():
   
    r = sr.Recognizer()

    with sr.Microphone() as source:
      print('Listening...')
      eel.DisplayMessage('Listening...')
      r.pause_threshold = 1
      r.adjust_for_ambient_noise(source)

      audio = r.listen(source, 10, 6)

    try:
      print('Recognizing')
      eel.DisplayMessage('Recognizing...')
      query = r.recognize_google(audio, language='en-in')
      print(f"user said: {query}")
      eel.DisplayMessage(query) 
    
      
    except Exception as e:
       return ""
    
    return query.lower()


@eel.expose
def allCommands(message=1):
   if message == 1:
      query = takecommand()
      print(query)
      eel.senderText(query)
   else:
       query = message
       eel.senderText(query)

   try:
   
      
      if "open" in query:
          from engine.features import openCommand
          openCommand(query)
      elif "on youtube" in query:
          from engine.features import PlayYoutube
          PlayYoutube(query)
      
      elif "time" in query:
          time=datetime.datetime.now().strftime('%I:%M %p')
          speak(time)

      elif "date" in query:
          date=datetime.datetime.now().strftime("%A, %B %d, %Y")
          speak(date)

      elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            message = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    message = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    message = 'call'
                else:
                    message = 'video call'
                    
                whatsApp(contact_no, query, message, name) 

                    
      else:
          from engine.features import chatBot 
          chatBot(query)         
   except:
      print("error")

   eel.ShowHood()



