from pyttsx3 import Engine

class MatchManager:
  def __init__(self):
    self.matchers_list = (
      {'type': 'converter', 'matchers': ('converta', 'converter')},
      {'type': 'translator', 'matchers': ('traduza', 'traduzir')},
      {'type': 'calculator', 'matchers': ('calcular', 'calcule')}
    )
    
  def look_for_matchers(self, sentence : str):
    for matcher_obj in self.matchers_list:
      for matcher in matcher_obj['matchers']:
        if sentence.find(matcher) != -1:
          return { 'type': matcher_obj['type'], 'matcher': matcher }
    return 'not_found'
  
  def execute_matcher_func(result, matcher_obj, robot : Engine):
    matcher_type = matcher_obj['type']
    matcher_word = matcher_obj['matcher']
    match matcher_type:
      case 'calculator':
        word_length = len(matcher_type)
        word_index = result.find(matcher_word)
        substring_index = word_index + word_length + 1

        calculation = result[substring_index:]

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
    
