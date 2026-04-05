def strip_password(x: dict[str, str]) -> None:
    try:
        del x['password']
    except KeyError:
        pass
