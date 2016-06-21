SQL = """
create table lookup
(
    md5 varchar unique not null,
    path varchar not null
);
"""


def up(db, conf):
    db.executescript(SQL)
