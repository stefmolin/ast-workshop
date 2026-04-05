def strip_password(x: dict[str, str]) -> None:
    try:
        print(f'Received dict with keys: {x.keys()}')
        try:
            del x['password']
        except KeyError:
            pass
    except Exception as e:
        raise TypeError('Invalid input, expected dict') from e
