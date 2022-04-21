import os
from model import GPTModel
from dataset import GPTDataset
from happytransformer import  GENTrainArgs
from cloud import OwnCloud
import argparse
import bz2
import shutil

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

    parser.add_argument("-m", "--model-version", help="Model version", type=str)
    parser.add_argument("-e", "--epochs", help="Training epochs", type=str)
    parser.add_argument("-l", "--learning-rate", help="Learning rate", type=str)
    parser.add_argument("-i", "--input-data", help="Input txt dataset", type=str)
    parser.add_argument("-o", "--output-folder", help="Output model folder", type=str)
    parser.add_argument("-p", "--pretrained", help="Output model folder", type=str)
    parser.add_argument("-c", "--cloud", help="Using OwnCloud", type=bool , default= False)
    
    args = parser.parse_args()
    
    load_path = None

    if args.input_data:
        path_to_txt = args.input_data
        if args.pretrained:
            load_path = args.pretrained
        if args.model_version:
            model_version = args.model_version
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
        if args.cloud:
            cloud = args.cloud
        else:
            cloud = False
    
    else:
        print('Please specify input data')
        exit()
    
    print(f'Model version: {model_version}')
    print(f'Epochs: {epochs}')
    print(f'Learning rate: {learning_rate}')
    print(f'Output folder: {path_to_output}')

    if cloud:
        print('Using OwnCloud')
        oc = OwnCloud()
        path_to_txt = oc.load_file(path_to_txt)



    try:
        model = GPTModel(model_version, load_path)
        trainer = GPTTrainer(path_to_txt, model)
        model = trainer.train(learning_rate=learning_rate , epochs=epochs)
        
        save_path = "./saved/"
        isExist = os.path.exists(save_path)

        if not isExist:
            os.makedirs(save_path)

        model.save(save_path + path_to_output)

        shutil.make_archive(save_path + path_to_output, 'bztar', save_path + path_to_output)

        if cloud:
            oc.put_file(save_path + path_to_output + '.tar.bz2', path_to_output + '.tar.bz2')
    
    except Exception as e:
        print(e)








    

    
