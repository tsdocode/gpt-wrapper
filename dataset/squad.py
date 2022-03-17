import json
from tqdm import tqdm


class SquadDataset():
    """Load squad from json format to txt format"""
   
    def __init__(self, path_to_json : str) -> None:
        print('Loading dataset...')
        self.json_squad = self.load_squad_json(path_to_json)

    def load_squad_json(self, path_to_json : str) -> dict:
        with open(path_to_json, 'r') as f:
            return json.load(f)
    
    def make_prompt(self, context : str, question: str, answer:str):
        sos , eos = '<s>\n' , '\n<\s>\n'
        return sos + f" context: {context} | question: {question} | answer: {answer}" + eos

    def to_txt_dataset(self):
        txt_data = ""
        for entity in tqdm(self.json_squad['data']):
            for paragraph in entity['paragraphs']:
                try:
                    context = paragraph['context']
                    # print(context)
                    for qas in paragraph['qas']:
                        question = qas['question']
                        answer = qas['answers'][0]['text']
                        txt_data += self.make_prompt(
                            context, question, answer
                        )
                except Exception as e:
                    pass
        return txt_data

    def save_txt(self, path_to_txt: str):
        with open(path_to_txt, 'w') as f:
            f.write(self.to_txt_dataset())
        print('Finished Loading dataset')
        return path_to_txt
