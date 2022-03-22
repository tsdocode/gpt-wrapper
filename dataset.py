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
    def save_txt(self, file_name):
        txt_data = self.to_txt()
        with open(file_name, 'w') as f:
            f.write(txt_data)
        return file_name

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", help="Input json file", type=str)
    parser.add_argument("-o", "--output-file", help="Output txt file", type=str)
    
    args = parser.parse_args()
    path_to_json = ""

    if args.input_file:
        path_to_json = args.input_file
        dataset = GPTDataset(path_to_json)
    if args.output_file:
        path_to_txt = args.output_file
        dataset.save_txt(path_to_txt)
    else:
        dataset.save_txt(path_to_json.replace('.json', '.txt'))

