import aiohttp
from . import __version__

URL = "https://ws.audioscrobbler.com/2.0/"


class LastFMException(Exception):
    def __init__(self, error, message)
        pass


class InvalidParamaters(LastFMException):
    pass


error_mapping = {
    6: InvalidParamaters
}


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
            
            if 200 < response.status < 300:
                return data

            error = data.get("error") 
            if error:
                raise error_mapping.get(error, LastFMException)(error, data.get("message"))
            

    async def get_recent_tracks(self, user: str, *, limit: int=10):
        return await self._request(Request("GET", "user.getRecentTracks", user=user, limit=limit))
