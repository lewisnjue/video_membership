from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
import pathlib # help me locate location of files 

from cassandra.cqlengine import connection

BASE_DIR = pathlib.Path(__file__).resolve().parent

ASTRADB_CONNECT_BUNDLE = BASE_DIR / "connect_bundle"/"connect.zip"
print(ASTRADB_CONNECT_BUNDLE) # -> see if the path exist 

ASTRADB_CLIENT_ID =""
ASTRADB_CLIENT_SECRET = ""

def get_session():
    cloud_config= {
    'secure_connect_bundle': 'secure-connect-video-membership.zip'
    }

    auth_provider = PlainTextAuthProvider(ASTRADB_CLIENT_ID, ASTRADB_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    connection.register_connection(str(session),session=session)
    connection.set_default_connection(str(session))

    return session
