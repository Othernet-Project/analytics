import json
import logging

from bottle import request, response, auth_basic

from .tasks import process_stats, LOOKUP_TABLE, LOOKUP_COLS


def collect_stats():
    data = request.forms.get('stream')
    supervisor = request.app.supervisor
    supervisor.exts.tasks.schedule(process_stats, args=(supervisor, data))
    return 'OK'


def check(username, password):
    conf = request.app.config
    return (username == conf['updates.username'] and
            password == conf['updates.password'])


@auth_basic(check)
def update_paths():
    try:
        data = json.load(request.body)
    except Exception:
        logging.exception("Update of known path hashes failed.")
        response.status = 400
    else:
        db = request.app.supervisor.exts.databases.reports
        q = db.Replace(LOOKUP_TABLE, cols=LOOKUP_COLS, constraints=('md5',))
        map_seq = (dict(md5=tup[0], path=tup[1]) for tup in data.items())
        db.executemany(q, map_seq)
        logging.info("Received {} new paths.".format(len(data)))
        return 'OK'


def routes(config):
    return (
        ('api:stats', collect_stats, 'POST', '/', {}),
        ('api:paths', update_paths, 'POST', '/updates/', {}),
    )
