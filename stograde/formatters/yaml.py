import yaml


def format_assignment_yaml(content) -> str:
    return '---\n' + yaml.safe_dump(content, default_flow_style=False)
