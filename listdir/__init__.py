import listdir.listdir
from listdir.listdir import setup_logging

setup_logging(default_path=os.path.join("/".join(__file__.split('/')[:-1]), 'config', 'loggingConfig.yaml')) #added to __init__.py