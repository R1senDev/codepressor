from typing  import TypeAlias, Any, Optional, Iterable
from types   import UnionType

import sys


_ClassInfo: TypeAlias = type | UnionType
ClassInfo: TypeAlias = type | UnionType | tuple[_ClassInfo, ...]


def log(
    *values: object,
    end:     str = '\n',
    sep:     str = ' '
) -> None:
    sys.stdout.write(sep.join(map(str, values)) + end)
    sys.stdout.flush()


def error(
    *values: object,
    end:     str = '\n',
    sep:     str = ' ',
    code:    Optional[int] = None
) -> None:
    sys.stderr.write(sep.join(map(str, values)) + end)
    sys.stderr.flush()
    if code is not None:
        exit(code)

def check_type(value: str, type_or_class: ClassInfo) -> None:
    if not isinstance(value, type_or_class):
        raise ValueError(f'invalid type: {value.__class__.__name__}')
    

def check_callability(value: object) -> None:
    if hasattr(value, '__call__'):
        return
    raise ValueError(f'is not callable')


def filter_dict(target: dict[Any, Any], keys: Iterable[Any]) -> None:
    remove_candidates = [key for key in target if key not in keys]
    for key in remove_candidates:
        del target[key]