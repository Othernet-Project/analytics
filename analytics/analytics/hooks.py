import json
import logging

import bottle

from .commands import stats_from_file


bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 * 10  # 10MB


def initialize(supervisor):
    try:
        with open(supervisor.config['updates.file'], 'r') as updates_file:
            data = json.load(updates_file)
    except Exception:
        logging.error('Known paths file could not be read.')
        supervisor.app.known_paths = dict()
    else:
        supervisor.app.known_paths = data

    supervisor.exts.commands.register(
        'import',
        stats_from_file,
        '--import',
        help="Imports stats from specified file."
    )
