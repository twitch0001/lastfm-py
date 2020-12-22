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
