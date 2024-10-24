from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
import pathlib # help me locate location of files 
from . import config 
from cassandra.cqlengine import connection

settings = config.get_settings()

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent # the location of the folder 

ASTRADB_CONNECT_BUNDLE = BASE_DIR / "connect_bundle"/"connect.zip"


ASTRADB_CLIENT_ID = settings.ASTRADB_CLIENT_ID # AUTHENTICATION TO CASSANDR
ASTRADB_CLIENT_SECRET = settings.ASTRADB_CLIENT_SECRET # AUTHENTICATION TO CASSANDRA
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
