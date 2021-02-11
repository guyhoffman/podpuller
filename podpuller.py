#!/usr/bin/env python

import feedparser

import configparser
import logging
from os.path import expanduser
from subprocess import run
import sys
from termcolor import cprint

from process import *
import ui

# Configuration Filename
config_filename = "~/.config/podpuller/feeds.conf"
directories = {}

logging.basicConfig(level=logging.INFO)


def update_configfile(conf):
    with open(expanduser(config_filename), "w") as configfile:
        conf.write(configfile)


def process_feed(feed_name, conf, be_quick):
    """Process Single Feed

    Args:
        feed_name (string): Name of feed to process
        conf (ConfigParser): We pass the config parser to update the file with RSS
         info and to read the defaults
    """
    feed = conf[feed_name]
    url = feed["URL"]
    keep = feed.getint("keep episodes", 0)

    rss = feedparser.parse(url)

    # Check for fetch / parse errors
    try:
        check_feederrors(rss)
    except Exception as e:
        logging.error("Erroneous feed URL: %s (%s)" % (url, type(e)))
        return

    cprint(f"  ====== {rss.feed.title} ({feed.name}; keep {keep}) ======  ", "grey", "on_yellow")

    # Serial podcasts need to be processed from last to first
    if feed.getboolean("serial"):
        rss.entries.reverse()

    #################################################
    # This is where the logic happens. Right now
    # single logic: always have the latest [keep] episodes
    #################################################
    dl_dir = directories["dl"]

    tobe_deleted = []
    if not be_quick:
        tobe_deleted = ui.mark_deletion(dl_dir + os.sep + feed.name)

    have = 0
    for episode in rss.entries:
        hash_episode(episode)

        if tobe_deleted and generate_filename(episode) in tobe_deleted:
            delete_episode(feed.name, episode, dl_dir)
            markPlayed(episode)
            continue

        if have < keep:
            if get_episode(feed.name, episode, dl_dir):
                have += 1
        else:
            delete_episode(feed.name, episode, dl_dir)

    # Post-processing Put podcast in config file it was just a URL
    if not "name" in feed:
        feed["name"] = rss.feed["title"]
        logging.info("Updating name in config")

    update_configfile(conf)


def sync_external():

    rsync_dir = directories["rsync"]
    dl_dir = directories["dl"]

    if os.path.exists(rsync_dir):
        if ui.yesno(f"Sync to player {rsync_dir}?"):
            run(["rsync", 
                "-vahxP", "--size-only", '--exclude=".*"', "--delete", expanduser(dl_dir), rsync_dir],
                capture_output=False,
            )
            logging.info("Done.")
    else:
        logging.info(f"Rsync destination {rsync_dir} not connected.")


def parse_dirs(config):
    s = config.default_section
    data_dir = config.get(s, "Data directory", fallback="=~/.local/share/podpuller")
    dl_dir = config.get(s, "Download directory", fallback="~/Downloads/podcasts/")
    rsync_dir = config.get(
        s, "MP3 Player directory", fallback="/Volumes/M500/podcasts/"
    )

    global directories
    directories["data"] = os.path.expanduser(data_dir)
    directories["dl"] = os.path.expanduser(dl_dir)
    directories["rsync"] = os.path.expanduser(rsync_dir)


def main():

    # Read feeds from config file
    conf = configparser.ConfigParser()
    conf.read(expanduser(config_filename))

    # Parse file location directories
    parse_dirs(conf)

    # Init DB
    init_db(directories["data"])
    logging.debug(list(Episode.select()))

    # Check for quick mode
    be_quick = False
    if conf.get(conf.default_section, "always quick", fallback=False) or ui.yesno(
        "Quick mode?"
    ):
        be_quick = True

    # If a feed ID is given, only process that feed
    if len(sys.argv) > 1:
        process_feed(sys.argv[1], conf, be_quick)
    else:
        # Process all feeds (except DEFAULT)
        for feed_name in conf:
            if feed_name != conf.default_section:
                process_feed(feed_name, conf, be_quick)

    logging.info("Done updating feeds.")

    # Try to sync to external drive (mp3 player)
    sync_external()


if __name__ == "__main__":
    main()
