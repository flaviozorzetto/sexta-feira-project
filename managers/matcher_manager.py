from pyttsx3 import Engine
from deep_translator import GoogleTranslator

class MatchManager:
  def __init__(self):
    self.matchers_list = (
      {'type': 'calculator', 'matchers': ('calcular', 'calcule')},
      {'type': 'translator', 'matchers': ('traduza', 'traduzir')},
      {'type': 'converter', 'matchers': ('converta', 'converter')},
    )
    
  def look_for_matchers(self, sentence : str):
    for matcher_obj in self.matchers_list:
      for matcher in matcher_obj['matchers']:
        if sentence.find(matcher) != -1:
          return { 'type': matcher_obj['type'], 'matcher': matcher }
    return 'not_found'
  
  def execute_matcher_func(self, result: str, matcher_obj, robot : Engine):
    matcher_type = matcher_obj['type']
    matcher_word = matcher_obj['matcher']
    word_length = len(matcher_word)
    word_index = result.find(matcher_word)
    substring_index = word_index + word_length + 1
    core_sentence = result[substring_index:]
    
    match matcher_type:
      # Calculos simples
      case 'calculator':
        calculation_split = core_sentence.split(' ')
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
      # Tradução de ingles para portugues
      case 'translator':
        translated = GoogleTranslator(source='portuguese', target='english').translate(core_sentence)
        robot.say(translated)
        robot.runAndWait()
      # Conversor de real para dólar
      case 'converter':
        converted_money = ("%.2f" % (float(core_sentence.split(' ')[1].replace(',', '.')) / 4.94))
        answer = str(converted_money) + ' dólares'
        print(answer)
        robot.say(answer)
        robot.runAndWait()