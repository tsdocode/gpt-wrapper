from model import GPTModel
from dataset.squad import SquadDataset
from happytransformer import  GENTrainArgs

class GPTTrainer():
    def __init__(self, path_to_json: str, model : GPTModel) -> None:
        self.model = model 
        self.path_to_json = path_to_json

    def train(self, learning_rate: float = 5e-5, epochs = 1):
        settings = GENTrainArgs(learning_rate=learning_rate, epochs=epochs)
        dataset = SquadDataset(self.path_to_json)
        path_to_txt = dataset.save_txt('./dataset/train.txt')
        self.model.train(path_to_txt, settings)

        return self.model