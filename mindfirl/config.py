import os


if 'DYNO' in os.environ:
    ENV = 'production'
else:
    ENV = 'development'

# data directory for virtual machine
# DATA_DIR = '/home/mindfirl/Documents/ppirl/MINDFIRL/mindfirl/data'
# data directory for dev
DATA_DIR = 'data'


DATA_PAIR_PER_PAGE = 6