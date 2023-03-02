import argparse
from preprocess import preprocess
from types import SimpleNamespace

import yaml
def readConfig(fp:str)->dict:
    with open(fp, "r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    return config



