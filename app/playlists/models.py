from datetime import datetime

import uuid
from app import config

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

settings = config.get_settings()

class Playlist(Model):
    __keyspace__ = settings.keyspace
    db_id = columns.UUID(primary_key = True,default= uuid.uuid1)
    user_id = columns.UUID()
    updated = columns.DateTime(default= datetime.utcnow())
    host_ids = columns.List(value_type=columns.Text)
    title = columns.Text()


    