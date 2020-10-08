import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
stopwords = set(stopwords.words("russian"))

import pymorphy2
morph = pymorphy2.MorphAnalyzer() 

import string

def text_lower(text): 
    return text.lower()

# remove punctuation 
def remove_punctuation(text): 
    translator = str.maketrans('', '', string.punctuation) 
    return text.translate(translator)

# remove outlayer numbers
def remove_outlayer_number(text):
      if len(text) == 8 or len(text) == 6:
          text = 'birth:' + '.'.join([text[:2],text[2:4],text[4:]]) # объединяем дату рождения

      elif text.startswith('19'): # проверяем год ли рождения 
          text = 'birth:'+ text
      else:
        text = float(text)
        if text >= 0. and text <= 31.0:
            text= 'date:' + str(int(text)) # скорее всего это праздник вроде 8 марта
        elif text >= 31. and text <= 110.:
            text= 'birth:'+ str(int(text))
        else:
            text =  'ERR'
            
      return text

def preprocess_text(text):
    '''
    Preprocesses text: 
    lowercase, tokenize, punctuation deletion, strange date deletion, overall cleaning

    Input:
    list of strings of sentences

    Returns:
    list of lists of tokens
    ''' 
    preprocessed_text = []
    # all to lowercase
    text = text_lower(text)  

    # sentence tokenize text                       
    sent_list = nltk.sent_tokenize(text, language="russian")  

    for sent in sent_list:

        #get rid of punctuation
        sent = remove_punctuation(sent)

        # get
        token_list = nltk.word_tokenize(sent, language='russian')
        morphed_list = [morph.parse(token)[0].normal_form for token in token_list if token not in stopwords]

        # check for strange numbers and delete them
        filtered_list = [remove_outlayer_number(token) if token.isdigit() else token  for token in morphed_list]

        # #dumb check for years of birth
        # filtered_list = [token]
        if 'ERR' in filtered_list: filtered_list.remove('ERR')
        preprocessed_text.append(filtered_list)

    return preprocessed_text

def create_intent_dict(text):
    ''' 
    Creates dict of intents. As a baseline

    Input:
    text is an array of arrays of strings

    Returns:
    intent_dict, dict

    intent_dict structure:
          {
            name: str, default:"бабушка"
            holiday: str (one of ['пасха', 'новый год', 'троица', 'день рождения', 
                                   '8 марта', 'рождество', 'юбилей'])  # TODO ADD MORE HOLIDAYS
            birth: str,
            date: str,
          }
    '''
    intent_dict = {}
    holiday_list = ['пасха', 'новый', 'троица', 'рождение', 
                    'март', 'рождество', 'юбилей']
    intent_dict['name'] = 'бабушка'

    text = preprocess_text(text) # предобрабатываем текст

    for sentence in text:
        for token in sentence:
            if token in holiday_list:
                if token == "рождение":
                  token = 'день '+ token
                if token == "новый":
                  token = token+ " год"
                intent_dict['holiday'] = token
            if token.startswith('birth'):
                intent_dict['birth'] = token.split(':')[1]
            if token.startswith('date'):
                intent_dict['date'] = token.split(':')[1]

    return intent_dict

