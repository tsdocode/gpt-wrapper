import json
from threading import local
from tqdm import tqdm
import argparse
from cloud import OwnCloud




class GPTDataset(object):
    def __init__(self, path_to_json: str, cloud = False) -> None:
        """Generate txt dataset from a json file.

        Args:
            path_to_json (str): Path to json file.
        """
        print('Loading dataset...')
        print(cloud)
        self.cloud = cloud
        if self.cloud:
            self.oc = OwnCloud()
        self.json_gpt = self.load_json(path_to_json)


        # print(self.json_gpt)

    def load_json(self, path_to_json: str):
        """Load json data from file"""
        if self.cloud:
            path_to_json = self.oc.load_file(path_to_json)

        with open(path_to_json, 'r') as f:
            # path_to_json = self.oc.load_file(path_to_json)
            return json.load(f)
            

    def make_prompt(self,split_token = ' | ' ,  **kwargs) -> None:
        """Make input prompt for GPT model

        Args:
            split_token (str, optional): Split symbot between two information. Ex: "question | answer". Defaults to ' | '.

        """
        sos , eos = "<|startoftext|>\n" ,  "\n<|endoftext|>\n"
        
        prompt_content = split_token.join([f"{value}" \
            for key, value in kwargs.items()])
        return sos + f"{prompt_content}" + eos
    
    def to_txt(self) -> str:
        """Convert json data to txt data.

        Returns:
            str: txt dataset
        """
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

    def save_txt(self, file_name: str) -> None:
        """Save txt data to file

        Args:
            file_name (str): output file name

        Returns:
            None
        """
        txt_data = self.to_txt()
        local_path = './' + file_name.split('/')[-1]

        print(local_path)

        with open(local_path,  'w') as f:
            f.write(txt_data)
        

        if self.cloud:
            self.oc.put_file(file_name, local_path)
        return file_name

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", help="Input json file", type=str)
    parser.add_argument("-o", "--output-file", help="Output txt file", type=str)
    parser.add_argument("-c", "--cloud", help="using OwnCloud", type=bool , default= False)

    
    args = parser.parse_args()
    path_to_json = ""


    if args.input_file:
        path_to_json = args.input_file
        dataset = GPTDataset(path_to_json, args.cloud)
    if args.output_file:
        path_to_txt = args.output_file
        dataset.save_txt(path_to_txt)
    else:
        dataset.save_txt(path_to_json.replace('.json', '.txt'))

