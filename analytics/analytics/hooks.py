from .commands import stats_from_file


def initialize(supervisor):
    supervisor.exts.commands.register(
        'import',
        stats_from_file,
        '--import',
        help="Imports stats from specified file."
    )
