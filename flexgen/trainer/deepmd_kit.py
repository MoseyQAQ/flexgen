import os 
import json
import numpy as np
from pathlib import Path
from glob import glob 
from flexgen.utils import get_machine_and_resources
from dpdispatcher import Machine, Resources, Task, Submission

'''
设计：
1. init函数：接受所有和训练本身无关的参数，包括machine, resources, command, iter, local_path, remote_path
2. make函数：接受和训练本身有关的参数，包括model_num, template_json, training_data，生成训练所需的文件
3. run函数：运行训练
4. post函数：后处理训练结果，包括收集训练好的模型，删除不必要的文件

'''
class DeepMDKit:
    def __init__(self, machine, resources, command: str, iter: int,
                 local_path: Path, remote_path: Path) -> None:
        '''
        Assign All staffs needed for deepmd-kit training, including:
            machine, resources, command, iteration number, local and remote path

        Args:
            machine: str or dpdispatcher.Machine
            resources: str or dpdispatcher.Resources
            command: command to run deepmd-kit
            iter: the iteration number
            local_path: local working path
            remote_path: remote path to run tasks
        '''
        self.command = command
        self.local_path = Path(local_path) if isinstance(local_path, str) else local_path
        self.remote_path = Path(remote_path) if isinstance(remote_path, str) else remote_path
        self.iter = iter
        self.working_path = local_path / Path(f'iter.{self.iter:02d}/01.train')
        self.machine, self.resources = get_machine_and_resources(machine, resources)

        if not os.path.exists(self.working_path):
            os.makedirs(self.working_path)
        else:
            print(f'Found old {self.working_path}')
    
    def make(self, model_num: int, template_json: str, training_data: list[str]) -> None:
        '''
        prepare for deepmd training, including generating training input files

        Args:
            model_num: number of models to train
            template_json: training template inputfile
            training_data: location of training data
        '''

        ####### prepare for deepmd training ######
        # check if template exists
        if not os.path.exists(template_json):
            raise FileNotFoundError(f'{template_json} not found')
        
        # load template
        training_template: dict=json.load(open(template_json, 'r'))

        # check if model_num is valid
        if model_num <= 0:
            raise ValueError('model_num should be greater than 0')
        
        # generate model_num random seeds
        random_seeds = np.random.randint(low=1000000, high=9999999, size=(model_num,4))

        # generate training input json content
        training_input = [training_template.copy() for i in range(model_num)]
        for i in range(model_num):
            training_input[i]['model']['descriptor']['seed'] = int(random_seeds[i][0])
            training_input[i]['model']['fitting_net']['seed'] = int(random_seeds[i][1])
            training_input[i]['training']['seed'] = int(random_seeds[i][2])
            if 'type_embedding' in training_input[i]['model']:
                training_input[i]['model']['type_embedding']['seed'] = int(random_seeds[i][3])
        
        ####### write training input ######
        # create dataset directory and link training data
        dataset_path = self.working_path / 'dataset'
        dataset_path.mkdir(exist_ok=True)
        for data in training_data:
            data_path  = Path(data).absolute()
            (dataset_path / data_path.name).symlink_to(data_path)

        # create model_num subdirectories, and write input.json files
        for i in range(model_num):
            model_path = self.working_path / f'model.{i:03d}'
            model_path.mkdir(exist_ok=True)
            input_dict = training_input[i]
            input_dict['training']['systems'] = [f'../dataset/{p.name}' for p in dataset_path.iterdir()]
            input_json_path = model_path / 'input.json'
            json.dump(input_dict, input_json_path.open('w'), indent=4)


        ####### create submission #######
        task_list = []
        for i in range(model_num):
            task = Task(command=self.command, 
                        task_work_path=f'model.{i:03d}',
                        forward_files=['input.json'],
                        backward_files=['train.log','lcurve.out','graph.pb'],
                        outlog='train.log',
                        errlog='train.log')
            task_list.append(task)
        
        self.submission = Submission(work_base=str(self.working_path.absolute()),
                                     machine=self.machine,
                                     resources=self.resources,
                                     task_list=task_list,
                                     forward_common_files=['dataset/'],
                                     backward_common_files=[])

    def run(self) -> None:
        '''run deepmd-kit training'''
        self.submission.run_submission()
    
    def post(self) -> None:
        '''post-process deepmd-kit training results: collect trained model
        delete unnecessary files
        '''
        raise NotImplementedError