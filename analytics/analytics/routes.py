import json
import logging

from bottle import request, response, auth_basic

from .tasks import process_stats


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
        # update in-memory store and then write complete data into file
        request.app.known_paths.update(data)
        with open(request.app.config['updates.file'], 'w') as updates_file:
            json.dump(request.app.known_paths, updates_file)
        logging.info("Received {} new paths.".format(len(data)))
        return 'OK'


def routes(config):
    return (
        ('api:stats', collect_stats, 'POST', '/', {}),
        ('api:paths', update_paths, 'POST', '/updates/', {}),
    )
