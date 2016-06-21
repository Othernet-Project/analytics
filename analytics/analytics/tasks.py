import logging
import uuid

from dateutil.tz import tzoffset

from bitpack.utils import bytes_to_hex
from .data import StatBitStream, DEVICE_ID_LENGTH


ANALYTICS_TABLE = 'stats'
LOOKUP_TABLE = 'lookup'
LOOKUP_COLS = ('md5', 'path')


def to_seconds(hours):
    return hours * 60 * 60


def uuidify(hex_string):
    return str(uuid.UUID(str(hex_string), version=4))


def process_stats(supervisor, data):
    device_id = uuidify(bytes_to_hex(data[:DEVICE_ID_LENGTH]))
    stats = StatBitStream.from_bytes(data[DEVICE_ID_LENGTH:])
    db = supervisor.exts.databases.reports
    lookup_query = db.Select(sets=LOOKUP_TABLE, where='md5 = %s')
    for entry in stats:
        path_hash = entry.pop('path', None)
        lookup_data = db.fetchone(lookup_query, (path_hash,))
        if not lookup_data:
            logging.error('Path hash not recognized: {}'.format(path_hash))
            continue
        data = dict(device_id=device_id, path=lookup_data['path'])
        data.update(entry)
        utc_timestamp = data['timestamp']
        local_tz = tzoffset(None, to_seconds(data['timezone']))
        # converting both timestamps into naive datetime objects because
        # postgres does not perform automatic conversion
        data['local_timestamp'] = (utc_timestamp.astimezone(local_tz)
                                                .replace(tzinfo=None))
        data['timestamp'] = utc_timestamp.replace(tzinfo=None)
        q = db.Replace(ANALYTICS_TABLE,
                       cols=data.keys(),
                       constraints=('timestamp', 'device_id', 'user_id'))
        db.execute(q, data)
    logging.debug("%s stat entries stored from %s", len(stats), device_id)
