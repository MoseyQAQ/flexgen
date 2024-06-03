import json 
import os 
import numpy as np

class Train:
    def __init__(self) -> None:
        raise NotImplementedError
    
    def make(self, data: dict) -> None:
        '''
        prepare for training

        Args:
            data: dict, training data parameters
        '''

        # get parameters from data dict
        engine: str=data['train']['engine']        # backend engine for training, default is deepmd
        model_num: int=data['train']['model_num']  # number of models to train
        template: str=data['training']['template'] # training template inputfile
        training_data: list[str]=data['training']['data'] # location of training data

        # 
        if engine == 'deepmd' or engine == 'dp':
            self.__make_deepmd(model_num, template, training_data)
        else:
            raise NotImplementedError
    
    def run(self) -> None:
        raise NotImplementedError
    
    def post(self) -> None:
        raise NotImplementedError
    
    def __make_deepmd(self, model_num: int, template: str, training_data: list[str]) -> None:
        '''
        prepare for deepmd training, including generating training input files

        Args:
            model_num: number of models to train
            template: training template inputfile
        '''

        # check if template exists
        if not os.path.exists(template):
            raise FileNotFoundError(f'{template} not found')
        
        # load template
        training_template: dict=json.load(open(template, 'r'))

        # check if model_num is valid
        if model_num <= 0:
            raise ValueError('model_num should be greater than 0')
        
        # generate model_num random seeds
        random_seeds = np.random.randint(low=1000000, high=9999999, size=(model_num,4))

        # generate training input files
        training_input = [training_template.copy() for i in range(model_num)]
        for i in range(model_num):
            training_input[i]['descriptor']['seed'] = random_seeds[i][0]
            training_input[i]['type_embedding']['seed'] = random_seeds[i][1]
            training_input[i]['fitting_net']['seed'] = random_seeds[i][2]
            training_input[i]['training']['seed'] = random_seeds[i][3]
            training_input[i]['training']['systems'] = training_data

