from typing import Any
import ml_helpers as mlh
from hypers import Hypers
from time import sleep

# Put all hyperparameters + paths in Args().
# - args only accepts (int, float, bool, str, list) types
# More complex objects are defined in init()
# - numpy arrays, dataloaders, tensors, pytorch models, optimizers, losses, etc

class Args(Hypers):
    # paths
    home_dir = '.'
    output_dir = '.'
    artifact_dir = './artifacts/'

    tags = ['example']

    # relative to home_dir
    data_dir = '/data'
    some_file = '/assets/example.csv'

    # Hyper params
    lr   = 0.001
    loss = 'adam'

    # Training settings
    epochs = 10
    seed   = 0
    cuda   = False
    layers = [1, 2, 3]

    # Add type declarations here for IDE autocomplete
    # for values that will be added in init()
    data: Any
    model: Any


# put all initialization logic here
def init(args: Args):
    args.config = args.to_dict() # save config for wandb before we add complex objects to args

    # This gives dot access to all paths, hyperparameters, etc
    args = mlh.default_init(args)

    # This makes all paths point in the right place
    args.data_dir, args.some_file = mlh.add_home(args.home_dir, args.data_dir, args.some_file)

    # get data
    # args.data = data_loader() or whatever

    # get model
    # args.model = model_loader() or whatever

    # add all other init logic here, like optimizers etc
    return args

# Main training loop
# adding explicit type declarations in each function for IDE autocomplete

def train(args: Args):
    loss = 0

    for epoch in range(args.epochs):
        loss += 1
        print(f'loss: {loss}, step: {epoch}')
        sleep(1)

    return loss

# Don't do this!!
# def train(data_dir, lr, epochs, cuda):
#     loss = 0
#     ....
# train(args.data_dir, args.lr, args.epochs, args.cuda)

# - unnecessary, and requires changing all function
#   signatures when you add a new hyperparameter

# Just pass args around instead:
# def train(args: Args):
#     print(args.data_dir)
#     loss = 0
#     ....

# train(args)
# - much cleaner, you can add new hyperparameters without changing
#   function signatures, and you get IDE autocompletion.

if __name__ == '__main__':
    loss = train(init(Args()))
    print(f'final loss: {loss}')

    # Run with:
    # python main.py config/default_params.py config/default_params2.py --tags=cat,dog,fish --layers=2,3,4,5 --use_dropout=true
