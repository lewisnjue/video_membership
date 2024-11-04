
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os

def get_session():
    cloud_config = {
        'cloud_config': {  # Assuming AstraDB configuration is provided through env vars
            'username': os.environ.get('CASSANDRA_USERNAME'),
            'password': os.environ.get('CASSANDRA_PASSWORD'),
            'hostname': os.environ.get('CASSANDRA_HOSTNAME'),
            'port': os.environ.get('CASSANDRA_PORT'),
        }
    }

    auth_provider = PlainTextAuthProvider(cloud_config['cloud_config']['username'], cloud_config['cloud_config']['password'])
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    return session