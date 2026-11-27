"""Read and write the content files (content/*.yml) in one consistent style,
so automatic changes show up as small, readable diffs."""
import os
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class _Dumper(yaml.SafeDumper):
    pass


def _str(d, s):
    if "\n" in s:
        return d.represent_scalar("tag:yaml.org,2002:str", s, style="|")
    return d.represent_scalar("tag:yaml.org,2002:str", s)


_Dumper.add_representer(str, _str)


def path(name):
    return os.path.join(ROOT, "content", name + ".yml")


def load(name):
    with open(path(name), encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save(name, data):
    with open(path(name), "w", encoding="utf-8") as f:
        yaml.dump(data, f, Dumper=_Dumper, allow_unicode=True, sort_keys=False, width=10 ** 6,
                  default_flow_style=False)
