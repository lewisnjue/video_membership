from algoliasearch.search.client import SearchClient
from app import config
from app.playlists.models import Playlist
from app.videos.models import Video
from .schemas import PlaylistIndexSchema, VideoIndexSchema

settings = config.get_settings()

# Correct way to get the index with Algolia Search Client 4.x.x
def get_index():
    client = SearchClient(settings.algolia_app_id, settings.algolia_api_key)
    return client

# Prepare the dataset by querying playlists and videos
def get_dataset():
    playlist_q = [dict(x) for x in Playlist.objects.all()]
    playlists_dataset = [PlaylistIndexSchema(**x).dict() for x in playlist_q]
    video_q = [dict(x) for x in Video.objects.all()]
    videos_dataset = [VideoIndexSchema(**x).dict() for x in video_q]
    dataset = videos_dataset + playlists_dataset
    return dataset

# Update the index with the dataset
def update_index():
    index = get_index()
    dataset = get_dataset()
    try:
        idx_resp = index.save_objects(dataset, {'autoGenerateObjectIDIfNotExist': True})
        idx_resp.wait()  # Wait until the indexing is complete
        count = len(idx_resp.raw_responses[0]['objectIDs'])
    except Exception as e:
        count = None
        print(f"Error while updating index: {e}")
    return count

# Perform a search on the index
def search_index(query):
    index = get_index()
    return index.search(query)
