import spotipy
import spotipy.util as util

class SpotipyAdaptor:
    def __init__(
        self,
        username,
        scope,
        client_id,
        client_secret,
        redirect_uri
    ):

        token = util.prompt_for_user_token(
            username,
            scope,
            client_id,
            client_secret,
            redirect_uri    
        )
        
        self.spotify_client = spotipy.client.Spotify(auth=token)


spotipy_adaptor = SpotipyAdaptor(
    username='114923525',
    scope='user-library-read user-top-read user-read-currently-playing user-read-recently-played',
    client_id='a5d677b7f92647b69ab65752478588d4',
    client_secret='07c5a3ddf0c745ca9a80b8a5ceb07dc0',
    redirect_uri='http://localhost/'
)

