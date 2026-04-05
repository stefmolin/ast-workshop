def strip_password(x: dict[str, str]) -> None:
    try:
        del x['password']
    except:
        pass


def strip_password_two(x: dict[str, str]) -> None:
    try:
        del x['password']
    except Exception:
        pass


def do_something(x: int) -> None:
    if not isinstance(x, int):
        raise Exception('Improper input format')


def do_something_else(x: int) -> None:
    if not isinstance(x, int):
        raise Exception


def do_another_thing(x: int) -> None:
    try:
        do_something(x)
    except:
        print('Shame on you!')
        raise
