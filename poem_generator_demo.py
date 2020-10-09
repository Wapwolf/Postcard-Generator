"""
DISCLAIMER : code uses poetru from http://pozdravok.ru. This content is not used for commercial use of any kind and solely belongs to it authors.
"""
import json
from random import randrange

def get_themed_poem(theme, poem_json = 'poetry.json'):
    """
    Returns random poem by theme
    Imput:
    theme, str - one of ['рождество', 'новый год', 'пасха', 'день рождения', 'троица', 'март', 'юбилей']
    Output:
    poem, str - randomly chosen themed poem
    """
    # Opening JSON file 
    with open(poem_json, 'r', encoding='utf-8') as json_file: 
        data = json.load(json_file) 

        return data[theme][str(randrange(5))] # get random poem
    
if __name__ == "__main__":
    get_themed_poem('рождество')