import yaml


def format_collected_data(content, debug):
    return '---\n' + yaml.safe_dump(content, default_flow_style=False)
