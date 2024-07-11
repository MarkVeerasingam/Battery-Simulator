import yaml

def load_batteryConfig(config_file="config/battery_chemistries.yaml"):
    with open(config_file, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None