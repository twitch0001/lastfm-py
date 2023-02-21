# lastfm-py
An asynchronous Python Last.FM API wrapper

## Installation

This project will be on PyPi once it is functional

Linux
```sh
python3 -m pip install -U lastfm-py
```
Windows
```sh
py -m pip install -U lastfm-py
```

## Examples

### Getting a user's recent scrobbles
```Python
import lastfm
import asyncio

client = lastfm.Client('client_key') # Replace with your client key (client_secret is optional)

async def main():
    recent_tracks = await client.get_recent_tracks("username", limit=5)
    print(recent_tracks[0].title) # prints the title of the users most recently scrobbled track

asyncio.run(main())
```


#### API Methods
|METHOD               |Implemented?|
|---------------------|------------|
|album.addTags        |No          |
|album.getInfo        |Yes         |
|album.getTags        |No          |
|album.getTopTags     |Yes         |
|album.removeTag      |No          |
|album.search         |Yes         |
|artist.addTags       |No          |
|artist.getCorrection |No          |
|artist.getInfo       |Yes         |
|artist.getSimilar    |No          |
|artist.getTags       |No          |
|artist.getTopAlbums  |No          |
|artist.getTopTags    |No          |
|artist.getTopTracks  |No          |
|artist.removeTag     |No          |
|artist.search        |No          |
|auth.getMobileSession |N/A         |
|auth.getSession      |No          |
|auth.getToken        |No          |
|chart.getTopArtists  |No          |
|chart.getTopTags     |No          |
|chart.getTopTracks   |No          |
|geo.getTopArtists    |No          |
|geo.getTopTracks     |No          |
|library.getArtists   |No          |
|tag.getInfo          |No          |
|tag.getSimilar       |No          |
|tag.getTopAlbums     |No          |
|tag.getTopArtists    |No          |
|tag.getTopTags       |No          |
|tag.getTopTracks     |No          |
|tag.getWeeklyChartList |No          |
|track.addTags        |No          |
|track.getCorrection  |No          |
|track.getInfo        |Yes         |
|track.getSimilar     |Yes         |
|track.getTags        |No          |
|track.getTopTags     |No          |
|track.love           |No          |
|track.removeTag      |No          |
|track.scrobble       |No          |
|track.search         |Yes         |
|track.unlove         |No          |
|track.updateNowPlaying |No          |
|user.getFriends      |Yes         |
|user.getInfo         |Yes         |
|user.getLovedTracks  |Yes         |
|user.getPersonalTags |Yes         |
|user.getRecentTracks |Yes         |
|user.getTopAlbums    |Yes         |
|user.getTopArtists   |Yes         |
|user.getTopTags      |Yes         |
|user.getTopTracks    |Yes         |
|user.getWeeklyAlbumChart |Yes         |
|user.getWeeklyArtistChart|Yes         |
|user.getWeeklyChartList |No          |
|user.getWeeklyTrackChart |Yes         |