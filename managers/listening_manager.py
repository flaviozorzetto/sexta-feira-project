from speech_recognition import Microphone, Recognizer
from pyttsx3 import Engine
from deep_translator import GoogleTranslator
from playsound import playsound
from datetime import datetime
import random, json, pathlib, os


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
      agenda_path = pathlib.Path('media/agenda.txt')
      calculate_matcher = ('calcular', 'calcule')
      translate_matcher = ('traduza', 'traduzir')
      converter_matcher = ('converta', 'converter')

      task_result = get_listen_result(recon, source)
      print('Frase ouvida: ' + task_result)
      # Agenda
      if task_result == 'cadastrar evento na agenda':
        robot.say('Ok, qual evento devo cadastrar')
        robot.runAndWait()
        event_result = get_listen_result(recon, source)
        if agenda_path.exists():
          file = open(agenda_path.absolute(), 'a')
          file.write(event_result + '\n')
          file.close()
        else:
            file = open(agenda_path.absolute(), 'w')
            file.write(event_result + '\n')
            file.close()
        robot.say('Evento cadastrado com sucesso')
        robot.runAndWait()
      elif task_result == 'ler agenda':
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
      elif task_result == 'cara ou coroa':
        sentences = ('Caiu cara dessa vez', 'Caiu coroa dessa vez')
        num = int(random.random() * 2)
        robot.say(sentences[num])
        robot.runAndWait()
      # Horario
      elif task_result == 'que horas são':
        now = datetime.now()
        result = str(now.hour) + ':' + str(now.minute)
        robot.say("O horário atual é " + result)
        robot.runAndWait()
      # Calculadora
      elif True if task_result.find(calculate_matcher[0]) != -1  or task_result.find(calculate_matcher[1]) != -1 else False:
        print('calculando')
        word_length = len(calculate_matcher)
        word_index = task_result.find(calculate_matcher)
        substring_index = word_index + word_length + 1

        calculation = task_result[substring_index:]

        calculation_split = calculation.split(' ')
        calculation_split[0] = int(calculation_split[0])
        calculation_split[2] = int(calculation_split[2])

        res = int

        match calculation_split[1]:
            case '+':
                res = calculation_split[0] + calculation_split[2]
            case '-':
                res = calculation_split[0] - calculation_split[2]
            case '*':
                res = calculation_split[0] * calculation_split[2]
            case 'x':
                res = calculation_split[0] * calculation_split[2]
            case '/':
                res = calculation_split[0] / calculation_split[2]
        
        robot.say('Resultado da conta é ' + str(res))
        robot.runAndWait()
      # Fato aleatório
      elif task_result == 'conte um fato aleatório':
        # Fonte https://escolaeducacao.com.br/curiosidades-conheca-agora-os-20-fatos-mais-aleatorios-de-todos/
        random_fact_list = ('O design de Yoda foi baseado e inspirado em Albert Einstein',
                            'Cães podem aprender a reconhecer um vocabulário de cerca de 165 palavras',
                            'Lulas gigantes tem os maiores olhos de qualquer animal na Terra',
                            'O governo australiano baniu a palavra “companheiro” por um dia')

        num = int(random.random() * len(random_fact_list))

        robot.say(random_fact_list[num])
        robot.runAndWait()
      # Tradução
      elif True if task_result.find(translate_matcher[0]) != -1 or task_result.find(translate_matcher[1]) != -1 else False:
        word_length = len(translate_matcher)
        word_index = task_result.find(translate_matcher)
        substring_index = word_index + word_length + 1

        to_translate_sentence = task_result[substring_index:]
        
        translated = GoogleTranslator(source='portuguese', target='english').translate(to_translate_sentence)
        
        robot.say(translated)
        robot.runAndWait()
      # Recomendação de filme
      elif task_result == 'recomende um filme' or task_result == 'recomenda um filme':
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
      elif task_result == 'tocar música':
        song_path = pathlib.Path('media/song.mp3').absolute()
        playsound(song_path)
      # Conversor de real para dólar
      elif True if task_result.find(converter_matcher[0]) != -1  or task_result.find(converter_matcher[1]) != -1 else False:
        for matcher in converter_matcher:
          if task_result.find(matcher) != -1:
            word_length = len(matcher)
            word_index = task_result.find(matcher)
            substring_index = word_index + word_length + 1

            to_convert_sentence = task_result[substring_index:]

            # Cotação dolar dia 05/05
            converted_money = ("%.2f" % (float(to_convert_sentence.split(' ')[1].replace(',', '.')) / 4.94))
            print('Dinheiro convertido: ' + (converted_money) + ' dólares')
            
            robot.say(str(converted_money) + ' dólares')
            robot.runAndWait()
      # Ano bissexto
      elif task_result == 'estamos no ano bissexto':
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
      elif task_result == 'desligar o computador':
        os.system("shutdown /s")
        
      restart_listen_handler(robot, recon, source, no_message=True)
    except KeyboardInterrupt:
      raise KeyboardInterrupt()
    except Exception:
      restart_listen_handler(robot, recon, source)