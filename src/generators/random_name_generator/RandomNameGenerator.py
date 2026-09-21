import json
from random import randint

class RandomNameGenerator:
    __names_loaded = False
    __names = []
    __count = 0
    
    @staticmethod
    def generate():
        if (not RandomNameGenerator.__names_loaded):
            RandomNameGenerator.load_names()
        
        index = randint(0, RandomNameGenerator.__count - 1)
        
        name = RandomNameGenerator.__names[index]
        
        return name
    
    @staticmethod
    def load_names():
        available_names = {}
        
        with open('src/generators/random_name_generator/available_names.json', 'r') as file:
            available_names = json.load(file)
        
        RandomNameGenerator.__names = available_names['names']
        RandomNameGenerator.__count = available_names['count']