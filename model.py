from happytransformer import HappyGeneration
from utils import default_preprocessing, default_posprocessing


class GPTModel():
    def __init__(self, model_version: str = '125M' , model_path : str = None)-> None : 
        print('Loading model...')
        if model_path:
            self.model = HappyGeneration(load_path=model_path)
        else:
            model_name = f"EleutherAI/gpt-neo-{model_version}"
            self.model = HappyGeneration("GPT-NEO" , model_name)
        self.train = self.model.train
        print('Loading model...')
        

    def save(self, path_to_model: str):
        self.model.save(path_to_model)

    def generate(self, schema: str, question: str,  preprocessing  = default_preprocessing , postprocessing = default_posprocessing):
        prompt = preprocessing(schema , question)
        result = self.model.generate_text(prompt).text
        return postprocessing(result)

    






