from __future__ import annotations

from .utils import filter_dict, check_type, check_callability

from os.path import join
from typing  import Any, Iterable, Callable, Generator
from io      import TextIOWrapper
from os      import listdir


def run_and_fetch(buffer: TextIOWrapper, names: Iterable[str]) -> dict[str, Any]:

    source = buffer.read()
    glocals: dict[str, Any] = {}

    try:
        exec(source, glocals)
    except Exception as exc:
        print(f'Error while running external code: {exc}')
        raise
    filter_dict(glocals, names)

    return glocals


class Plugin:

    class LoadError(ValueError): ...

    def __init__(
        self,
        title:       str,
        description: str,
        authors:     tuple[str, ...],
        version:     tuple[int, ...],
        exts:        tuple[str],
        processor:   Callable[[str], str]
    ) -> None:
        
        self.title       = title
        self.authors     = authors
        self.description = description
        self.version     = version
        self.exts        = exts
        self.process     = processor

    @classmethod
    def from_source(cls, buffer: TextIOWrapper) -> Plugin:

        glocals = run_and_fetch(buffer, (
            '__title__',
            '__desc__',
            '__authors__',
            '__version__',
            '__exts__',
            'process'
        ))

        check_type(glocals['__title__'],   str)
        check_type(glocals['__desc__'],    str)
        check_type(glocals['__authors__'], tuple)
        check_type(glocals['__version__'], tuple)
        check_type(glocals['__exts__'],    tuple)
        check_callability(glocals['process'])

        return cls(
            glocals['__title__'],
            glocals['__desc__'],
            glocals['__authors__'],
            glocals['__version__'],
            glocals['__exts__'],
            glocals['process']
        )

    def __str__(self) -> str:
        return f'Plugin["{self.title}"]'


class PluginsSpace:

    allowed_title_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYS0123456789_'

    class StagingError(KeyError): ...
    class RegisteringError(ValueError): ...

    def __init__(self, *plugins: Plugin) -> None:

        self.plugins: dict[str, Plugin] = {}
        self.exts:    dict[str, str]    = {}
        
        for plugin in plugins:
            self.register_plugin(plugin)

    def validate_title(self, title: str) -> bool:
        if title == '':
            return False
        
        for char in title:
            if char not in self.allowed_title_chars:
                return False
            
        return True

    def register_plugin(self, target: Plugin) -> None:

        if target.title in self.plugins:
            raise self.__class__.RegisteringError(f'plugin titled "{target.title}" is already registered in this {self.__class__.__name__}')

        if not self.validate_title(target.title):
            raise self.__class__.RegisteringError(f'plugin\'s title is invalid')

        for ext in target.exts:
            self.exts[ext] = target.title
        
        self.plugins[target.title] = target

    def get_plugin_by_title(self, title: str) -> Plugin:

        try:
            return self.plugins[title]
        except KeyError:
            raise self.__class__.StagingError(f'cannot find plugin: "{title}"')

    def get_plugin_by_target_fname(self, fname: str) -> Plugin:

        for ext, title in self.exts.items():
            if fname.endswith(ext):
                return self.plugins[title]
        
        raise self.__class__.StagingError(f'cannot find eligible plugin for "{fname}"')
    
    def plugin_iter(self) -> Generator[Plugin, None, None]:

        for plugin in self.plugins.values():
            yield plugin


def scan_folder(path: str) -> list[str]:

    results: list[str] = []
    
    for fname in listdir(path):

        if not fname.endswith('.py') or fname.startswith('_'):
            continue

        results.append(join(path, fname))

    return results