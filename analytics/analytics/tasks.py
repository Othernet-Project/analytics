import logging

from .bitstream import bytes_to_hex
from .data import StatBitStream, DEVICE_ID_LENGTH


ANALYTICS_TABLE = 'stats'


def process_stats(supervisor, data):
    device_id = bytes_to_hex(data[:DEVICE_ID_LENGTH])
    stats = StatBitStream.from_bytes(data[DEVICE_ID_LENGTH:])
    db = supervisor.exts.databases.reports
    for entry in stats:
        data = dict(device_id=device_id)
        data.update(entry)
        q = db.Insert(ANALYTICS_TABLE, cols=data.keys())
        db.execute(q, data)
    logging.debug("%s stat entries stored from %s", len(stats), device_id)
