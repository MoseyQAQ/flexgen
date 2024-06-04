import os 
import json
import numpy as np
from pathlib import Path
from glob import glob 
from flexgen.utils import get_machine_and_resources
from dpdispatcher import Machine, Resources, Task, Submission

class LAMMPS:
    def __init__(self, machine, resources, command: str, iter: int,
                 local_path: Path, remote_path: Path) -> None:
        self.command = command
        self.local_path = Path(local_path) if isinstance(local_path, str) else local_path
        self.remote_path = Path(remote_path) if isinstance(remote_path, str) else remote_path
        self.iter = iter
        self.working_path = local_path / Path(f'iter.{self.iter:02d}/03.sample')
        self.machine, self.resources = get_machine_and_resources(machine, resources)

        if not os.path.exists(self.working_path):
            os.makedirs(self.working_path)
        else:
            print(f'Found old {self.working_path}')
    
    def make(self, temps: list[float], press: list[float], trj_freq: int, nsteps: int, ensemble: str,
             template_input: str=None, variables: dict=None) -> None:
        pass

    def run(self) -> None:
        pass

    def post(self) -> None:
        pass