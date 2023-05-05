from deep_translator import GoogleTranslator
from speech_recognition import Microphone, Recognizer
from pyttsx3 import Engine
from playsound import playsound
from datetime import datetime
import random, json, pathlib, os
from managers.matcher_manager import MatchManager

agenda_path = pathlib.Path('media/agenda.txt')

def restart_listen_handler(robot, recon, source, custom_message = 'Algo deu errado, tente de novo do começo', no_message = False):
  if not no_message:
    robot.say(custom_message)
    robot.runAndWait()
  listen_handler(robot, recon, source)

# Para facilitar fiz com que o retorno fosse sempre em minusculo para comparativo de frases para execução dos diferentes métodos
def get_listen_result(recon : Recognizer, source : Microphone):
  audio = recon.listen(source, timeout=3, phrase_time_limit=10)
  res = str.lower(recon.recognize_google(audio, language='pt'))
  return res 

def listen_handler(robot : Engine, recon : Recognizer, source : Microphone, layer = 0):
  if layer == 0:
    print("Ouvindo camada de reconhecimento de sexta-feira (layer 0)")
    try:
      result = get_listen_result(recon, source)
      # As vezes ela entende 'cesta' ou 'cesto' em vez de sexta
      sexta_recognizer_sentences = ('ok sexta-feira', 'sexta-feira', 'sexta', 'cesta', 'cesto', 'ok sexta', 'ok cesta', 'ok cesto') 
      found = False
      for sentence in sexta_recognizer_sentences:
        if sentence == result:
          found = True
          listen_handler(robot, recon, source, 1)
          break
      if not found:
        restart_listen_handler(robot, recon, source, 'Não entendi, repita novamente')
    except KeyboardInterrupt:
      raise KeyboardInterrupt()
    except Exception:
      restart_listen_handler(robot, recon, source)
      
  if layer == 1:
    robot.say('Sim mestre. O que deseja')
    robot.runAndWait()
    print("Ouvindo camada de reconhecimento da tarefa (layer 1)")
    try:
      task_result = get_listen_result(recon, source)
      print('Frase ouvida: ' + task_result)
      
      match_manager = MatchManager()
      result_from_matchers = match_manager.look_for_matchers(task_result)
      if result_from_matchers != 'not_found':
        match_manager.execute_matcher_func(task_result, result_from_matchers, robot)
      else:
        match task_result:
          # Agenda
          case 'cadastrar evento na agenda':
            robot.say('Ok, qual evento devo cadastrar')
            robot.runAndWait()
            event_result = get_listen_result(recon, source)
            
            file = open(agenda_path.absolute(), 'a' if agenda_path.exists() else 'w')
            file.write(event_result + '\n')
            file.close()

            robot.say('Evento cadastrado com sucesso')
            robot.runAndWait()
          case 'ler agenda':
            if agenda_path.exists():
              file = open(agenda_path.absolute(), 'r')
              file_content = file.read()
              file.close()
              robot.say(file_content)
              robot.runAndWait()
            else:
              robot.say('Ainda não foram cadastrados nenhum evento')
              robot.runAndWait()
          # Cara ou coroa
          case 'cara ou coroa':
            sentences = ('Caiu cara dessa vez', 'Caiu coroa dessa vez')
            num = int(random.random() * 2)
            robot.say(sentences[num])
            robot.runAndWait()
          # Horario
          case 'que horas são':
            now = datetime.now()
            result = str(now.hour) + ':' + str(now.minute)
            robot.say("O horário atual é " + result)
            robot.runAndWait()
          # Fato aleatório
          case 'conte um fato aleatório':
            # Fonte https://escolaeducacao.com.br/curiosidades-conheca-agora-os-20-fatos-mais-aleatorios-de-todos/
            random_fact_list = ('O design de Yoda foi baseado e inspirado em Albert Einstein',
                                'Cães podem aprender a reconhecer um vocabulário de cerca de 165 palavras',
                                'Lulas gigantes tem os maiores olhos de qualquer animal na Terra',
                                'O governo australiano baniu a palavra “companheiro” por um dia')
            num = int(random.random() * len(random_fact_list))

            robot.say(random_fact_list[num])
            robot.runAndWait()
          # Recomendação de filme
          case 'recomende um filme' | 'recomenda um filme':
            movie_path = pathlib.Path('media/movies.json').absolute()
            f = open(movie_path)
            
            data = json.load(f)
            movies_length = len(data['movies'])

            selected_movie = data['movies'][int(random.random() * movies_length)]

            movie_title = selected_movie['title']
            movie_plot = selected_movie['plot']
            movie_year = selected_movie['year']

            translated_movie_plot = GoogleTranslator(source='english', target='portuguese').translate(movie_plot)

            movie_descriptor = 'O filme se chama ' + movie_title + ' e é de ' + movie_year + ' possuindo a seguinte descrição:\n' + translated_movie_plot
            
            robot.say(movie_descriptor)
            robot.runAndWait()

            f.close()
          # Tocar uma música
          case 'tocar música':
            song_path = pathlib.Path('media/song.mp3').absolute()
            playsound(song_path)
          # Ano bissexto
          case 'estamos no ano bissexto':
            year = datetime.now().year
            year_verifier = lambda year : (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
            if year_verifier(year):
              robot.say('Estamos no ano bissexto')
              robot.runAndWait()
            else:
              found_correct_year = False
              while not found_correct_year:
                year += 1
                if year_verifier(year):
                  found_correct_year = True
              robot.say('Não é ano bissexto\n' + 'Próximo ano sera em ' + str(year))
              robot.runAndWait()
          # Desligar o computador
          case 'desligar o computador':
            os.system("shutdown /s")
      restart_listen_handler(robot, recon, source, no_message=True)
    except KeyboardInterrupt:
      raise KeyboardInterrupt()
    except Exception:
      restart_listen_handler(robot, recon, source)