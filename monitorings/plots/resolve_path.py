import pathlib

def resolve_path(path):
    if not pathlib.Path(path).is_absolute():
        return pathlib.Path(path).resolve()
    return path