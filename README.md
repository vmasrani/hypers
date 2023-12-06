# Hypers: Simplified Hyperparameter Management

Hypers is a lightweight Python class designed to simplify the management of machine learning hyperparameters. It abstracts away the complexities of using argparse, providing a more intuitive and user-friendly interface.

## Features
- **Automatic command line access**: Hypers automatically integrates with argparse, inferring types and providing command line access to your hyperparameters.
- **Pretty printing**: Hypers automatically prints your hyperparameters in a color-coded format upon instantiation, making it easy to see the current configuration at a glance.
- **Config file support**: You can define additional configuration files and pass them as command line arguments.
- **Conversion to dictionary**: Hypers can convert your hyperparameters to a dictionary, making it easy to upload them to platforms like Weights & Biases.
- **Minimalistic and extendable**: Hypers is less than 150 lines of code and uses only Python Standard Library packages, making it easy to understand, modify, and extend.

## Usage

### From argparse to Hypers

Hypers turns this:
```python
import argparse

parser = argparse.ArgumentParser(description='Demo script for defining random hyperparameters')

parser.add_argument('--learning_rate', type=float, default=0.01, help='Learning rate for the model')
parser.add_argument('--batch_size', type=int, default=32, help='Batch size for training')
parser.add_argument('--use_dropout', action='store_true', help='Whether to use dropout in the model')
parser.add_argument('--optimizer', type=str, default='adam', choices=['adam', 'sgd', 'rmsprop'], help='Optimizer for training')
parser.add_argument('--hidden_layers', type=int, nargs='+', default=[256, 128], help='Sizes of hidden layers')
parser.add_argument('--tags', type=str, nargs='+', default=['cat', 'dog'], help='Sizes of hidden layers')

args = parser.parse_args()
lr = args.learning_rate
print(args)
```

Into this:

```python 
from hypers import Hypers

class Args(Hypers):
    learning_rate = 0.01 # types automatically inferred
    batch_size = 32
    use_dropout = True
    optimizer = 'adam'
    hidden_layers = [256, 128] # types inferred in lists too
    tags = ['cat','dog'] # types inferred in lists too

    args = Args()
    lr = args.learning_rate # maintains dot access

args = Args()
config = args.to_dict() # to upload to wandb
lr = args.learning_rate # maintains dot access
```

### Using Config Files

You can define additional configuration files and pass them as command line arguments:

```bash
python main.py config/default_params.py config/default_params2.py --tags=cat,dog,fish --layers=2,3,4,5 --use_dropout=true
```
## Installation

Hypers is a standalone Python file with no additional dependencies. Just copy the `hypers.py` file it into your project and import it. Protip: Rather than copying `hypers.py` into every new project, create a hidden directory in home (i.e. `~/.python`) and set your `PYTHONPATH` in your bashrc via `export PYTHONPATH=~/.python:$PYTHONPATH`. 

Then you can `import hypers from Hypers` in all your projects. Super handy to prevent the case where you have K slightly modified copies of hypers.py and you've tweaked a few of them.

See example and intended usage in main.py
## Contributing

Contributions to Hypers are welcome! Please submit a pull request or open an issue on GitHub.

