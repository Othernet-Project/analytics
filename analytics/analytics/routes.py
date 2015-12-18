from bottle import request

from .tasks import process_stats


def collect_stats():
    data = request.forms.get('stream')
    supervisor = request.app.supervisor
    supervisor.exts.tasks.schedule(process_stats, args=(supervisor, data))
    return 'OK'


def routes(config):
    return (
        ('api:stats', collect_stats, 'POST', '/', {}),
    )
