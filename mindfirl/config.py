import os


if 'DYNO' in os.environ:
    ENV = 'production'
else:
    ENV = 'development'