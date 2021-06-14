import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lastfm-py",
    version="0.0.12",
    author="twitch7443",
    author_email="twitch7443@pm.me",
    description="An asynchronous LastFM API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/twitch0001/lastfm-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requries=">=3.6"
)
