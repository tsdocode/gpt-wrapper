from ast import arg
from ensurepip import version
from json import load
from model import GPTModel
from dataset import GPTDataset
from happytransformer import  GENTrainArgs
import argparse

class GPTTrainer():
    def __init__(self, path_to_txt: str, model : GPTModel) -> None:
        """Load model and dataset for training

        Args:
            path_to_txt (str): Path to txt dataset
            model (GPTModel): GPT-NEO version or local_path
        """
        self.model = model 
        self.path_to_txt = path_to_txt

    def train(self, learning_rate: float = 5e-5, epochs = 1):
        print('Training model...')
        settings = GENTrainArgs(learning_rate=learning_rate, num_train_epochs=epochs)
        self.model.train(self.path_to_txt, settings)
        print('Finished training model, you can save it now using model.save()')

        return self.model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--model-version", help="Model version", type=str)
    parser.add_argument("-e", "--epochs", help="Training epochs", type=str)
    parser.add_argument("-l", "--learning-rate", help="Learning rate", type=str)
    parser.add_argument("-i", "--input-data", help="Input txt dataset", type=str)
    parser.add_argument("-o", "--output-folder", help="Output model folder", type=str)
    parser.add_argument("-p", "--pretrained", help="Output model folder", type=str)
    
    args = parser.parse_args()
    
    load_path = None

    if args.input_data:
        path_to_txt = args.input_data
        if args.pretrained:
            load_path = args.pretrained
        if args.model_version:
            model_version = args.model-version
        else:
            model_version = '125M'
        if args.epochs:
            epochs = int(args.epochs)
        else:
            epochs = 1
        if args.learning_rate:
            learning_rate = float(args.learning_rate)
        else:
            learning_rate = 5e-5
        if args.output_folder:
            path_to_output = args.output_folder
        else:
            path_to_output = path_to_txt.split('.')[0]
    
    else:
        print('Please specify input data')
        exit()
    
    print(f'Model version: {model_version}')
    print(f'Epochs: {epochs}')
    print(f'Learning rate: {learning_rate}')
    print(f'Output folder: {path_to_output}')


    model = GPTModel(model_version, load_path)
    trainer = GPTTrainer(path_to_txt, model)
    model = trainer.train(learning_rate=learning_rate , epochs=epochs)
    model.save('./saved/' + path_to_output)






    

    
