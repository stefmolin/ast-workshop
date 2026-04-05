import json
from contextlib import suppress


def strip_password(x):
    with suppress(KeyError):
        del x['password']


def dump_info(x, out):
    json.dump(strip_password(x), out)


def analyze_something(x):
    import pandas as pd

    df = pd.DataFrame(x)
