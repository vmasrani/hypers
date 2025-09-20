from typing import Any, List
from hypers import Hypers, TBD
from dataclasses import dataclass


@dataclass
class Args(Hypers):
    # paths
    home_dir: str = '.'
    output_dir: str = '.'
    artifact_dir: str = './artifacts/'

    # relative to home_dir
    data_dir: str = '/data'
    some_file: str = '/assets/example.csv'

    # Hyper params
    lr: float = 0.001
    loss: str = 'adam'

    # Training settings
    epochs: int = 10
    seed: int = 0
    cuda: bool = False

    # Add type declarations here for IDE autocomplete
    # for values that will be added in init()
    data: Any = TBD()
    model: Any = TBD()

if __name__ == '__main__':
    args = Args()
    print(f'final loss: {args}')
