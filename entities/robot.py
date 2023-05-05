import pyttsx3

def createRobot(voice, rate, volume):
  r = pyttsx3.init()
  r.setProperty('voice', voice)
  r.setProperty('rate', rate)
  r.setProperty('volume', volume)
  return r