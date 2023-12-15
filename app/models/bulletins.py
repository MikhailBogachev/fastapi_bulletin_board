from datetime import datetime

import sqlalchemy 

from .users import users_table


metadata = sqlalchemy.MetaData()


bulletin_types_table = sqlalchemy.Table(
    "bulletin_types",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50), nullable=False)
)


bulletins_table = sqlalchemy.Table(
    "bulletins",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.TIMESTAMP, default=datetime.utcnow),
    sqlalchemy.Column("type", sqlalchemy.ForeignKey("bulletin_types.id")),
    sqlalchemy.Column("author_id", sqlalchemy.ForeignKey(users_table.c.id))
)
