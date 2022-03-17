from happytransformer import HappyGeneration
from utils import default_preprocessing, default_posprocessing


class GPTModel():
    def __init__(self, model_version: str = '125M' , model_path : str = None)-> None : 
        if model_path:
            self.model = HappyGeneration(load_path=model_path)
        else:
            self.model = HappyGeneration("GPT-NEO" , f"EleutherAI/gpt-neo-{model_version}")



    def save(self, path_to_model: str):
        self.model.save(path_to_model)

    def generate(self, context: str, question: str , preprocessing : function = default_preprocessing , postprocessing: function = default_posprocessing):
        prompt = preprocessing(context , question)
        result = self.model.generate_text(prompt).text
        return postprocessing(result)

    






