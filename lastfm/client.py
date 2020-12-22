import aiohttp
from . import __version__
from .errors import LastFMException, mapping

URL = "https://ws.audioscrobbler.com/2.0/"


class Request:
    def __init__(self, method, path, **extra):
        self.method = method
        self.path = path  # The Last.FM API method but my naming sucks

        self.extra = extra


async def json_or_text(response):
    if response.headers["Content-Type"] == "application/json":
        return await response.json()
    return await response.text()


class Client:
    def __init__(self, client_key: str, client_secret: str = None):
        self._key = client_key 
        self._secret = client_secret

        self._session = None
        self.user_agent = "Lastfm-py / {0} (https://github.com/twitch0001/lastfm-py)".format(__version__)

    async def _request(self, request):
        if not self._session:  # ClientSession init requires async
            self._session = aiohttp.ClientSession()

        headers = {
            "User-Agent": self.user_agent
        } 
        
        params = {
            "format": "json",
            "api_key": self._key, 
            "method": request.path
        }
        params.update(request.extra)  # Update with method specific params
        async with self._session.request(request.method, URL, params=params) as response:
            data = await json_or_text(response)
            print(response.status)
            
            if 200 <= response.status < 300:
                return data

            error = data.get("error") 
            if error:
                raise mapping.get(error, LastFMException)(error, data.get("message"))
        
            return data

    # > User methods <
    async def get_info(self, user: str=None):
        """user.getInfo - user defaults to session auth"""
        return await self._request(Request("GET", "user.getInfo", user=user))

    async def get_recent_tracks(self, user: str, *, limit: int=10):
        return await self._request(Request("GET", "user.getRecentTracks", user=user, limit=limit))
    
    async def get_top_tracks(self, user: str, period: str=None, *, limit: int=10, page: int=0):
        return await self._request(Request("GET", "user.getTopTracks", user=user, limit=limit))

    async def get_top_artists(self, user: str, period: str=None, *, limit: int=10, page: int=0):
        return await self._request(Request("GET", "user.getTopArtists", user=user, limit=limit))

    async def get_top_albums(self, user: str, period: str=None, *, limit: int=10, page: int=0):
        return await self._request(Request("GET", "user.getTopAlbums", user=user, limit=limit))

