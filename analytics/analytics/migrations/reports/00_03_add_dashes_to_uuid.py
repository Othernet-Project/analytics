import uuid


def uuidify(hex_string):
    return str(uuid.UUID(str(hex_string), version=4))


def up(db, conf):
    q = db.Select(sets='stats')
    for row in db.fetchiter(q):
        update_query = db.Update('stats',
                                 device_id='%(device_id)s',
                                 where='id = %(id)s')
        db.execute(update_query, dict(id=row['id'],
                                      device_id=uuidify(row['device_id'])))
