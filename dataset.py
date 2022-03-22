import json
from tqdm import tqdm
import argparse


class GPTDataset(object):
    def __init__(self, path_to_json: str):
        print('Loading dataset...')
        self.json_gpt = self.load_json(path_to_json)
        # print(self.json_gpt)

    def load_json(self, path_to_json: str):
        with open(path_to_json, 'r') as f:
            return json.load(f)

    def make_prompt(self,split_token = ' | ' ,  **kwargs):
        sos , eos = "<|startoftext|>\n" ,  "\n<|endoftext|>\n"
        
        prompt_content = split_token.join([f"{key}: {value}" \
            for key, value in kwargs.items()])
        return sos + f"{prompt_content}" + eos
    
    def to_txt(self):
        txt_data = ""
        for sample in tqdm(self.json_gpt['data']):
            try:
                # print(sample)
                prompt = self.make_prompt(**sample)
                txt_data += prompt
            except Exception as e:
                pass
        # print(txt_data[:300])
        return txt_data

if __name__ == '__main__':
    test = GPTDataset('./test.json')
    # print(test.make_prompt(schema = '2' , question = '3', sql='4'))
    print(test.to_txt())