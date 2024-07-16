import yaml

def load_battery_config(config_file="config/battery_chemistries.yaml"):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None

battery_config = load_battery_config()
