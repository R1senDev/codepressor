__title__   = 'compress_js_like'
__desc__    = 'Compresses JS, TS, JSON and similar languages'
__authors__ = ('R1senDev',)
__version__ = (0, 1, 0)
__exts__    = ('.js', '.ts', '.json')


def process(source: str) -> str:

    from re import sub, finditer

    SUB_CHAR = '\x1a'

    # Preserving strings
    strings: dict[str, str] = {}
    for m in finditer(r'(\'(?:[^\'\\]|\\.)*\'|\"(?:[^\"\\]|\\.)*\"|\`(?:[^\`\\]|\\.)*\`)', source):
        key = f'{SUB_CHAR}{str(len(strings)).zfill(5)}'
        string = m.group(1)
        strings[key] = string
        source = source.replace(string, key)

    # Replacing newlines
    source = sub(
        r'\s*[\n]\s*',
        '',
        source
    )

    # Squashing spaces
    source = sub(
        r'\s*([\(\)\[\]\{\}=:+-/*])\s*',
        lambda m: m.group(1),
        source
    )

    # Recovering strings
    for pair in strings.items():
        source = source.replace(*pair)

    return source