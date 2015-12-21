SQL = """
ALTER TABLE stats ADD UNIQUE (device_id, user_id, timestamp);
"""


def up(db, conf):
    db.executescript(SQL)
