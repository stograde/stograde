from logging import warning
import yaml


def load_config():
    has_config = False
    with open('.cs251toolkitrc.yaml', 'a+', encoding='utf-8') as config_file:
        config_file.seek(0)
        try:
            contents = config_file.read()
        except OSError as err:
            warning(err)
            return

    if not contents:
        contents = ''

    try:
        config = yaml.safe_load(contents)
    except:
        config = {}

    if not config:
        config = {}
    else:
        has_config = True

    return has_config, config


def save_config(conf):
    with open('.cs251toolkitrc.yaml', 'w', encoding='utf-8') as config_file:
        contents = yaml.safe_dump(conf, default_flow_style=False)
        config_file.write(contents)
