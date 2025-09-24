__title__   = 'template'
__desc__    = 'Template plugin. Does nothing.'
__authors__ = ('R1senDev',)
__version__ = (1, 0, 0)
__exts__    = ('.file',)


def process(source: str) -> str:
    return 'Hello World!'