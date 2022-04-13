from ast import arg
import pandas as pd
from happytransformer import HappyGeneration , GENSettings
from server.gpt.preprocessing import *
from server.gpt.postprocess import *
from server.gpt.wrapper.model import GPTModel

few_shot = """"
<param>
"""
model_distinct = HappyGeneration(load_path='./server/gpt/pretrained_model/baseline')

model = GPTModel(model_path='./server/gpt/pretrained_model/baseline')


model_dict = {
    'baseline' : model,
}



def generate_code(schema , question, settings):
    model_ver = settings['model_ver']
    model = model_dict[model_ver]
    sql = model.generate(schema, question)

    return sql

if __name__ == '__main__':
    print(generate_code(schema="a", question="b",settings={'model_ver':'baseline'}))





