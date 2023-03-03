def readConfig(fp:str)->dict:
    import yaml
    with open(fp, "r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    return config