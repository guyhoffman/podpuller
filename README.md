# podpuller

### A simple python app to sync your podcasts with RSS feeds and transfer to an external MP3 player

After giving up my smartphone and buying a cheapo MP3 player I wanted a way to keep my feeds synced. 

There are many great programs for this out there, like [Greg](https://github.com/manolomartinez/greg/), but it didn't really fit my workflow, which was having a certain number of episodes of each podcast, and manually marking the ones I have alreaedy listened to. 

This is that app. It was heavily inspired (and liberally copied) from the exellent [upodder](https://github.com/m3nu/upodder) which is no longer maintained. 

## Workflow

1. Choose your RSS feeds
2. Specify how many episodes you want
3. If desired, mark the ones you listened to
4. Sync
5. If desired, transfer to external drive

The config file is read from `~/.config/podpuller/feeds.conf` and you have an example [here](https://github.com/guyhoffman/podpuller/blob/main/feeds.example.conf). It is pretty straightforward. 

- `data directory`: Where to store the SQL database of downloaded and listened episodes
- `download directory`: Where to download the podcasts to. 
- `mp3 player directory`: Where to sync the download directory to. 

## Notes

- Every podcast goes into a directory named by its config file section (for example `tal` in the example).
- Sync both transfers and deletes files. It basically does an exact copy.
- All defaults, including `rsync` flags, are for MacOS but can probably be easily changed for UN*X systems.
- No need to provide a name for the feed, just a URL, the name will be auto-filled from the RSS feed.

## Roadmap

- Tag MP3 files with info from feed
- UI improvements
- Handle "oldest-first" workflow for serial podcasts
