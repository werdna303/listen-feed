# Listen (private podcast feed)

Half-hour teaching episodes for morning runs. Served by GitHub Pages as a podcast feed.

Feed URL (paste into Apple Podcasts > Library > ... > Follow a Show by URL):
https://werdna303.github.io/listen-feed/feed.xml

The feed carries `itunes:block` so Apple will not list it in the public directory.

## Add episodes
1. Put `slug.mp3` and `slug.txt` in `episodes/` (the first line of the .txt is the title).
2. `python3 build_feed.py https://werdna303.github.io/listen-feed/`
3. Commit and push. New episodes appear in the app within a few hours (pull down to refresh sooner).
