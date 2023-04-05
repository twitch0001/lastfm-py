from __future__ import annotations

import datetime
import uuid
from typing import Optional, List


class Date:
    def __init__(self, data: dict):
        self.unix_timestamp: int = int(data.get("uts") or data.get("unixtime"))  # can either be uts or unixtime
        self.text: str = data["#text"]

        self.datetime: datetime.datetime = datetime.datetime.fromtimestamp(self.unix_timestamp)

    def __str__(self) -> str:
        return self.text

    def __int__(self) -> int:
        return self.unix_timestamp

    def __repr__(self) -> str:
        return '<Date timestamp={uts} text={text}>'.format(uts=self.unix_timestamp, text=self.text)


class Image:
    def __init__(self, data: dict):
        self.size: str = data["size"]
        self.text: str = data["#text"]

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return '<Image size={size} url={url}>'.format(size=self.size, url=self.text)


class PartialEntity:
    def __init__(self, data: dict):
        self.name: str = data.get("#text") or data.get("name")
        self.mbid: Optional[uuid.SafeUUID] = data.get("mbid")

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return '<Entity name={name} mbid={mbid}>'.format(name=self.name, mbid=self.mbid)


class PartialAlbum(PartialEntity):
    def __init__(self, data: dict):
        super().__init__(data)

        self.artist: PartialEntity = PartialEntity(data["artist"])
        self.images: List["Image"] = [Image(d) for d in data.get("image", [])]


class PartialArtist(PartialEntity):
    def __init__(self, data: dict):
        super().__init__(data)

        self.images: List["Image"] = [Image(d) for d in data.get("image", [])]


class PartialTrack:
    def __init__(self, data: dict):
        self.artist: PartialEntity = PartialEntity(data["artist"])
        self.streamable: bool = data.get("streamable", False)   # Figure out way of making this a model? it's a couple of different things
        self.images: List["Image"] = [Image(d) for d in data.get("image", [])]
        self.mbid: Optional[uuid.SafeUUID] = data.get("mbid")
        self.name: str = data["name"]
        self.url: str = data["url"]
        self.duration: int = data.get("duration", 0)
        date = data.get("date")
        self.date: Optional["Date"] = Date(data["date"]) if date else None


    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return '<PartialTrack name={name} artist={artist}>'.format(name=self.name, artist=self.artist)


class TopModelAttributes:
    def __init__(self, data: dict):
        self.rank: int = data.get("rank")


class TopAlbum(PartialAlbum):
    def __init__(self, data: dict):
        super().__init__(data)

        self.playcount: Optional[int] = data.get("playcount", 0)
        self.attr: TopModelAttributes = TopModelAttributes(data.get("@attr", {}))


class TopArtist(PartialArtist):
    def __init__(self, data: dict):
        super().__init__(data)

        self.playcount: Optional[int] = data.get("playcount", 0)
        self.attr: TopModelAttributes = TopModelAttributes(data.get("@attr", {}))


class TopTrack(PartialTrack):
    def __init__(self, data: dict):
        super().__init__(data)

        self.playcount: Optional[int] = data.get("playcount", 0)
        self.attr: TopModelAttributes = TopModelAttributes(data.get("@attr", {}))


class RecentTrackAttributes:
    def __init__(self, data: dict):
        self.now_playing: bool = data.get("nowplaying", False)


class RecentTrack(PartialTrack):
    def __init__(self, data: dict):
        super().__init__(data)
        self.album: PartialEntity = PartialEntity(data["album"])
        self.attr: RecentTrackAttributes = RecentTrackAttributes(data.get("@attr", {}))


    def __repr__(self) -> str:
        return '<Track name={name} artist={artist}>'.format(name=self.name, artist=self.artist)


class PageAttributes:
    def __init__(self, data: dict):
        self.per_page: int = data["perPage"]
        self.total_pages: int = data["totalPages"]
        self.page: int = data["page"]
        self.scrobbles: int = data["total"]
        self.user: str = data["user"]

    def __repr__(self) -> str:
        return '<Attr page={page} per_page={per_page} pages={pages}>'.format(page=self.page, per_page=self.per_page, pages=self.total_pages)


class Paged:
    def __init__(self, data: dict):
        self.attr: PageAttributes = PageAttributes(data["@attr"])


class User:
    def __init__(self, data: dict):
        self.name: str = data.get("name")
        self.age: int = data.get("age")
        self.subscriber: bool = bool(int(data.get("subscriber", 0)))
        self.real_name: str = data.get("realname")
        self.bootstrap: str = data.get("bootstrap")
        self.playcount: int = data.get("playcount")  # total scrobbles
        self.artist_count: int = data.get("artist_count")
        self.playlists: int = data.get("playlists")
        self.track_count: int = data.get("track_count")
        self.album_count: int = data.get("album_count")

        self.images: List[Image] = [Image(image) for image in data.get("image", [])]
        self.registered_at: Date = Date(data.get("registered"))
        self.country: str = data.get("country")
        self.gender: str = data.get("gender")
        self.url: str = data.get("url")
        self.type: str = data.get("type")


    def __repr__(self) -> str:
        return '<User username={username} playcount={playcount}>'.format(username=self.name, playcount=self.playcount)


class RecentTracks(Paged):
    def __init__(self, data: dict):
        super().__init__(data["recenttracks"])
        self.tracks: List[RecentTrack] = [RecentTrack(d) for d in data["recenttracks"]["track"]]

    def __len__(self) -> int:
        return len(self.tracks)

    def __repr__(self) -> str:
        return '<RecentTracks attr={attr}>'.format(attr=self.attr)

    def __getitem__(self, item: int) -> RecentTrack:
        return self.tracks[item]


class Friends(Paged):
    def __init__(self, data: dict):
        super().__init__(data["friends"])
        self.friends: List[User] = [User(user) for user in data["friends"]["user"]]


class LovedTracks(Paged):
    def __init__(self, data: dict):
        super().__init__(data["lovedtracks"])
        self.tracks: List[PartialTrack] = [PartialTrack(track) for track in data["lovedtracks"]["track"]]


class TopAlbums(Paged):
    ...


class TopArtists(Paged):
    ...


class TopTracks(Paged):
    ...
