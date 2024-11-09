from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
from . import config 
from cassandra.cqlengine import connection

settings = config.get_settings() # the result of this function will be cached by lru_cache from functool which is very very cool 
ASTRADB_CONNECT_BUNDLE_PATH = settings.base_dir.parent   

ASTRADB_CONNECT_BUNDLE =ASTRADB_CONNECT_BUNDLE_PATH  / "connect_bundle"/"connect.zip"

ASTRADB_CLIENT_ID = settings.db_client_id # AUTHENTICATION TO CASSANDR
ASTRADB_CLIENT_SECRET = settings.db_client_secret # AUTHENTICATION TO CASSANDRA
def get_session():
    cloud_config= {
    'secure_connect_bundle': ASTRADB_CONNECT_BUNDLE
    }

    auth_provider = PlainTextAuthProvider(ASTRADB_CLIENT_ID, ASTRADB_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    connection.register_connection(str(session),session=session)
    connection.set_default_connection(str(session))
    return session
