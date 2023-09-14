import yaml


class quoted(str):
    pass


def quoted_presenter(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')


def write_yml(input_sheet: dict, file_path: str) -> None:
    file = open("file_path", "w")
    yaml.dump(
        input_sheet, file, indent=4, default_flow_style=False, explicit_start=True
    )
    file.close()
    print("YAML file saved.")
