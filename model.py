from happytransformer import HappyGeneration
from utils import default_preprocessing, default_posprocessing


class GPTModel():
    def __init__(self, model_version: str = '125M' , model_path : str = None)-> None : 
        """Load GPT-Neo model

        Args:
            model_version (str, optional): params version of GPT-NEO. Defaults to '125M'.
            model_path (str, optional): Load pretrained model from file. Defaults to None.
        """
        print('Loading model...')
        if model_path:
            self.model = HappyGeneration(load_path=model_path)
        else:
            model_name = f"EleutherAI/gpt-neo-{model_version}"
            self.model = HappyGeneration("GPT-NEO" , model_name)
        self.train = self.model.train
        print('Done!')
        

    def save(self, path_to_model: str):
        """Save model 

        Args:
            path_to_model (str): Path to save model
        """
        self.model.save(path_to_model)

    def generate(self, schema: str, question: str,  preprocessing  = default_preprocessing , postprocessing = default_posprocessing):
        """Generate SQL from schema and question 

        Args:
            schema (str): table schema (column names and datatype)
            question (str): Input question
            preprocessing (_type_, optional): Preprocessing function . Defaults to default_preprocessing.
            postprocessing (_type_, optional): Postprocessing function. Defaults to default_posprocessing.

        Returns:
            _type_: _description_
        """
        prompt = preprocessing(schema , question)
        result = self.model.generate_text(prompt).text
        return postprocessing(result)

    






