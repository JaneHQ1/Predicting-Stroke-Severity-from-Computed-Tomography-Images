from tensorboardX import SummaryWriter
import os

checkpoint_dir = './logs'
lr = 1e-2

if not os.path.isdir(checkpoint_dir):
    os.makedirs(checkpoint_dir)

writer = SummaryWriter(os.path.join(checkpoint_dir, 'exp_{}'.format(lr)))
