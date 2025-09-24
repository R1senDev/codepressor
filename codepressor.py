from argparse import ArgumentParser
from sys      import argv

from core.plugins import PluginsSpace, Plugin, scan_folder
from core.utils   import log, error


ap = ArgumentParser()
ap.add_argument(
    'action',
    choices = ('process', 'list'),
    help    = 'What you want this program to do.'
)
ap.add_argument(
    'target',
    help = 'Action subject.'
)
ap.add_argument(
    'output',
    nargs   = '?',
    default = None,
    help    = 'Path to the output file.'
)
ap.add_argument(
    '-p', '--plugin',
    default = None,
    help    = 'Forcefully uses plugin, restricting codepressor to choose it automatically.'
)
args = ap.parse_args(argv[1:])


plugins = PluginsSpace()
plugins_fnames = scan_folder('plugins/')
for plugin_fname in plugins_fnames:
    with open(plugin_fname, 'r') as file:
        plugin = Plugin.from_source(file)
    plugins.register_plugin(plugin)


match args.action:

     
    case 'process':

        if args.plugin is None:
            try:
                target_plugin = plugins.get_plugin_by_target_fname(args.target)
            except PluginsSpace.StagingError as exc:
                error(f'{exc.__class__.__name__}: {str(exc).strip("'")}')
                exit(0) # Calling explicitly to shut up static checkers and stuff
        else:
            target_plugin = plugins.get_plugin_by_title(args.plugin)

        with open(args.target, 'r') as file:
            source = file.read()

        result = target_plugin.process(source)

        if args.output is None:
            log(result)
            exit(0)

        with open(args.output, 'w') as file:
            file.write(result)


    case 'list':

        match args.target:

            case 'plugins':

                for plugin in plugins.plugin_iter():

                    assigned_to = 'nothing'
                    if plugin.exts:
                        assigned_to = ', '.join([ext for ext in plugin.exts]) + ' files'

                    log(
                        f'- {plugin.title} v{'.'.join(map(str, plugin.version))}',
                        f'    {plugin.description}',
                        f'    Created by {', '.join(map(str, plugin.authors))}',
                        f'    Assigned to process {assigned_to}',
                        sep = '\n',
                        end = '\n\n'
                    )

                log('Notice: the earlier a plugin appears in this list, the higher its priority.')

            case _:
                error(f'Invalid target for list: "{args.target}"', code = 0)


    case 'fetch':
        error('Not implemented!', code = 0)

        match args.target:

            case 'logs':
                error('Not implemented!', code = 0)

            case _:
                error(f'Invalid target for fetch: "{args.target}"', code = 0)

    case _:
        error('Invalid action:', args.action, code = 0)