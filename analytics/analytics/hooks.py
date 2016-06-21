import bottle

from .commands import stats_from_file


bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 * 10  # 10MB


def initialize(supervisor):
    supervisor.exts.commands.register(
        'import',
        stats_from_file,
        '--import',
        help="Imports stats from specified file."
    )
