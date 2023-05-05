import speech_recognition as sr
from entities.robot import createRobot
from managers.listening_manager import listen_handler

robot = createRobot('brasil', 180, 1)
recon = sr.Recognizer()

with sr.Microphone() as source:
  recon.adjust_for_ambient_noise(source, duration=1.5)
  try:
    listen_handler(robot, recon, source)
  except KeyboardInterrupt:
    print('KeyboardInterrupt error')
  finally:
    print('Ending program')