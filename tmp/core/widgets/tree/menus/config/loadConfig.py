import yaml

configurationFile = '/home/adam/code/lura/lura/core/widgets/tree/menus/config/config.yaml'

def getConfiguration(menu): 
    with open(configurationFile, 'r') as stream:
        config = yaml.safe_load(stream)
        if menu in config: return config[menu]
