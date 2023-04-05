import logging
from typing import Optional

import aiohttp

from . import __version__
from .errors import LastFMException, mapping

log = logging.getLogger(__name__)

URL = "https://ws.audioscrobbler.com/2.0/"


# https://github.com/Rapptz/discord.py/blob/6265723a352ee77f418ef3004012cc5693ba390f/discord/http.py#L274
class Request:
    def __init__(self, method, path, **extra):
        self.method = method
        self.path = path  # The Last.FM API method but my naming sucks

        self.extra = extra


# https://github.com/Rapptz/discord.py/blob/6265723a352ee77f418ef3004012cc5693ba390f/discord/http.py#L100
async def json_or_text(response):
    if response.headers["Content-Type"] in ("application/json", "application/json; charset=UTF-8"):  # pain...
        return await response.json()
    return await response.text()


class Client:
    """Client for making requests to Last.FM

    Parameters 
    ----------
    client_key: str
        Your Last.fm key
    client_secret: Optional[str]
        Your Last.fm secret. Only used for User authentication (TODO)

    **session: Optional[aiohttp.ClientSession]
        The ClientSession to use for Requests (set at your own risk)
    **user_agent: Optional[str]
        The User-Agent header that will be sent in requests
    """

    def __init__(self, client_key: str, client_secret: str = None, *, session: aiohttp.ClientSession = None, user_agent: str = None):
        self._key: str = client_key
        self._secret: str = client_secret

        self._session: Optional[aiohttp.ClientSession] = None or session
        self.user_agent: str = user_agent or "Lastfm-py / {0} (https://github.com/twitch0001/lastfm-py)".format(__version__)

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._session

    async def _request(self, request: Request):
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
        async with self._session.request(request.method, URL, headers=headers, params=params) as response:
            data = await json_or_text(response)
            log.debug("Method: %s returned status: %s data: %s", request.path, response.status, data)
            if isinstance(data, str):
                raise LastFMException(0, data)

            if 200 <= response.status < 300:
                return data

            error = data.get("error")
            if error:
                raise mapping.get(error, LastFMException)(error, data.get("message"))

            return data

    # > User methods <

    async def user_get_info(self, user: str) -> dict:
        """

        Parameters
        ----------
        user: str

        Returns
        -------

        """
        return await self._request(Request("GET", "user.getInfo", user=user))

    async def user_get_friends(self, user: str, *, recent_tracks: bool = False, limit: int = 50, page: int = 1) -> dict:
        """Gets a users Friends
        Parameters
        ----------
        user: str
        recent_tracks: bool
        limit: int (default: 50)
        page: int (default: 1)

        Returns
        -------

        """
        return await self._request(Request("GET", "user.getFriends", user=user, recenttracks=str(recent_tracks), limit=limit, page=page))

    async def user_get_loved_tracks(self, user: str, *, limit: int = 50, page: int = 1) -> dict:
        """

        Parameters
        ----------
        user: str
        limit: int (default: 50)
        page: int (default: 1)

        Returns
        -------

        """
        return await self._request(Request("GET", "user.getLovedTracks", user=user, limit=limit, page=page))

    async def user_get_personal_tags(self, user: str, tag: str, tagging_type: str, *, limit: int = 50, page: int = 1) -> dict:
        """

        Parameters
        ----------
        user: str
        tag: str
        tagging_type: str
        limit: int (default: 50)
        page: int (default: 1)

        Returns
        -------

        """
        fields = {
            "user": user,
            "tag": tag,
            "limit": limit,
            "page": page,
            "taggingtype": tagging_type
        }

        return await self._request(Request("GET", "user.getPersonalTags", **fields))

    async def user_get_recent_tracks(self, user: str, *, limit: int = 10, page: int = 1, extended: bool = False, **extra) -> dict:
        """

        Parameters
        ----------
        user: str
        limit: int (default: 50)
        page: int (default: 1)
        extended: bool (default: False)
        start: Optional[int]
        to: Optional[int]

        Returns
        -------
        """
        fields = {
            "user": user,
            "limit": limit,
            "page": page,
            "extended": int(extended)  # query params cannot be booleans because
        }
        if "start" in extra: 
            fields["from"] = extra["start"]

        if "to" in extra:
            fields["to"] = extra["to"]

        return await self._request(Request("GET", "user.getRecentTracks", **fields))

    async def user_get_top_albums(self, user: str, period: str = "overall", *, limit: int = 10, page: int = 1) -> dict:
        """

        Parameters
        ----------
        user: str
        period: str (default: "overall")
        limit: int (default: 10)
        page: int (default: 1)

        Returns
        -------

        """
        return await self._request(Request("GET", "user.getTopAlbums", user=user, limit=limit, period=period, page=page))

    async def user_get_top_artists(self, user: str, period: str = "overall", *, limit: int = 10, page: int = 1) -> dict:
        """

        Parameters
        ----------
        user: str
        period: str (default: "overall")
        limit: int (default: 10)
        page: int (default: 1)

        Returns
        -------

        """
        return await self._request(Request("GET", "user.getTopArtists", user=user, limit=limit, period=period, page=page))

    async def user_get_top_tags(self, user: str, *, limit: int = 50) -> dict:
        """

        Parameters
        ----------
        user: str
        limit: int (default: 10)

        Returns
        -------

        """
        return await self._request(Request("GET", "user.getTopTags", user=user, limit=limit))

    async def user_get_top_tracks(self, user: str, period: str = "overall", *, limit: int = 10, page: int = 1) -> dict:
        """

        Parameters
        ----------
        user: str
        period: str (default: "overall")
        limit: int (default: 10)
        page: int (default: 1)

        Returns
        -------

        """
        return await self._request(Request("GET", "user.getTopTracks", user=user, limit=limit, period=period, page=page))

    async def user_get_weekly_artist_chart(self, user: str, *, limit: int = 10, page: int = 1, **extra) -> dict:
        """

        Parameters
        ----------
        user: str
        limit: int (default: 10)
        page: int (default: 1)
        start: Optional[int]
        to: Optional[int]

        Returns
        -------

        """
        fields = {
            "user": user,
            "limit": limit,
            "page": page,
        }
        if "start" in extra:
            fields["from"] = extra["start"]

        if "to" in extra:
            fields["to"] = extra["to"]

        return await self._request(Request("GET", "user.getWeeklyArtistChart", **fields))

    async def user_get_weekly_album_chart(self, user: str, *, limit: int = 10, page: int = 1, **extra) -> dict:
        """

        Parameters
        ----------
        user: str
        limit: int (default: 10)
        page: int (default: 1)
        start: Optional[int]
        to: Optional[int]

        Returns
        -------

        """
        fields = {
            "user": user,
            "limit": limit,
            "page": page,
        }
        if "start" in extra:
            fields["from"] = extra["start"]

        if "to" in extra:
            fields["to"] = extra["to"]

        return await self._request(Request("GET", "user.getWeeklyAlbumChart", **fields))

    async def user_get_weekly_track_chart(self, user: str, *, limit: int = 10, page: int = 1, **extra) -> dict:
        """

        Parameters
        ----------
        user: str
        limit: int (default: 10)
        page: int (default: 1)
        start: Optional[int]
        to: Optional[int]

        Returns
        -------

        """
        fields = {
            "user": user,
            "limit": limit,
            "page": page,
        }
        if "start" in extra:
            fields["from"] = extra["start"]

        if "to" in extra:
            fields["to"] = extra["to"]

        return await self._request(Request("GET", "user.getWeeklyTrackChart", **fields))

    async def user_get_weekly_chart_list(self, user: str) -> dict:
        """Get a list of available charts for the user
        Parameters
        ----------
        user: str - username of the user

        Returns
        -------
        dict
        """
        return await self._request(Request("GET", "user.getWeeklyChartList", user=user))


    def _track_shortcut(self, method, **fields):
        valid_fields = ("track", "artist", "mbid", "username", "autocorrect")
        params = {
            k: v for k, v in fields.items() if k in valid_fields
        }
        return self._request(Request("GET", method, **params))
    
    async def track_get_info(self, **fields) -> dict:
        """

        Parameters
        ----------
        fields

        Returns
        -------

        """
        return await self._track_shortcut("track.getInfo", **fields) 
    
    async def track_get_similar(self, **fields) -> dict:
        """

        Parameters
        ----------
        fields

        Returns
        -------

        """
        return await self._track_shortcut("track.getSimilar", **fields) 

    async def track_search(self, track: str, *, limit: int = 30, page: int = 1, **extra) -> dict:
        """

        Parameters
        ----------
        track
        limit
        page
        extra

        Returns
        -------

        """
        fields = {
            "track": track,
            "page": page,
            "limit": limit
        }

        if "artist" in extra:
            fields["artist"] = extra["artist"]

        return await self._request(Request("GET", "track.Search", **fields))

    async def artist_get_info(self, **fields) -> dict:
        """

        Parameters
        ----------
        fields

        Returns
        -------

        """
        valid_fields = ("track", "artist", "mbid", "username", "autocorrect")
        params = {
            k: v for k, v in fields.items() if k in valid_fields
        }
        return await self._request(Request("GET", "artist.getInfo", **params))
    
    async def album_get_info(self, **fields) -> dict:
        """

        Parameters
        ----------
        fields

        Returns
        -------

        """
        valid_fields = ("album", "artist", "mbid", "username", "autocorrect", "lang")
        params = {
            k: v for k, v in fields.items() if k in valid_fields
        }
        return await self._request(Request("GET", "album.getInfo", **params))

    async def album_get_top_tags(self, **fields) -> dict:
        """

        Parameters
        ----------
        fields

        Returns
        -------

        """
        valid_fields = ("album", "artist", "mbid", "autocorrect")
        params = {
            k: v for k, v in fields.items() if k in valid_fields
        }
        return await self._request(Request("GET", "album.getTopTags", **params))

    async def album_search(self, album: str, *, limit: int = 30, page: int = 1) -> dict:
        """

        Parameters
        ----------
        album: str
        limit: int (default: 50)
        page: int (default: 1)

        Returns
        -------

        """
        return await self._request(Request("GET", "album.Search", album=album, limit=limit, page=page))
