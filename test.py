from hypers import Hypers

class Args(Hypers):
    learning_rate = 0.01 # types automatically inferred
    batch_size = 32
    use_dropout = True
    optimizer = 'adam'
    hidden_layers = [256, 128] # types inferred in lists too
    tags = ['cat','dog'] # types inferred in lists too

args = Args()
config = args.to_dict() # to upload to wandb
lr = args.learning_rate # maintains dot access
