import json 
import os 
import numpy as np
from flexgen.trainer.deepmd_kit import DeepMDKit


class Train:
    def __init__(self) -> None:
        raise NotImplementedError
    
    def make(self, data: dict) -> None:
        '''
        prepare for training: generate training input files

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
            self.trainer = DeepMDKit()
        else:
            raise NotImplementedError
    
    def run(self) -> None:
        raise NotImplementedError
    
    def post(self) -> None:
        raise NotImplementedError

