#!/usr/bin/env python3

# Terminal bot - post a random terminal status, based on the info in 
# the wonderful Terminal Wiki. This work is a remix of that, also under
# the same licence, i.e. CC BY-SA 3.0).

import random
import json
import time
import sys

delay = 60 * 60 * 24 # seconds in a day
datafile = './terminals.json'
testmode = "--test" in sys.argv

# If we're in test mode, reduce the delay to 5 secs. If we're
# not in test mode, set up for the Mastodon API calls.
if (testmode):
    delay = 2
else:
    from mastodon import Mastodon
    mastodon = Mastodon(
        access_token = 'token.secret',
        api_base_url = 'https://botsin.space/'
    )

# Read in the terminals data and set the initial list
with open(datafile) as f:
    data = json.load(f)
terminals = data.copy()

# Go on forever, picking the next terminal each time around. Remove
# each picked terminal from the list to avoid repeated consecutive
# posts; refill the list when it gets empty.
while True:

    # Pick the first terminal in the list then remove it
    choice = 0
    terminal = terminals[choice]
    del terminals[choice]

    # If we're down to zero in the list, refill it
    if len(terminals) <= 0:
        terminals = data.copy()

    # Set up the text for the post:
    # - Title (make & model)
    # - An attribute picked at random
    # - Attribution and link to more info

    title = " ".join([terminal["make"], terminal["model"]])

    attributes = list(terminal["attributes"])
    attribute_key = attributes[random.randrange(len(attributes))]
    attribute_val = terminal["attributes"][attribute_key]

    status = "\n".join([
        title,
        ": ".join([" ".join(attribute_key.split("-")), attribute_val]),
        "Courtesy of the Terminals Wiki. More details: " + terminal["source"]
    ])

    # Emit the status, locally if in test mode, otherwise via a new post
    if (testmode):
        print(status)
    else:
        media = mastodon.media_post("./images/" + terminal["image"])
        mastodon.status_post(status, media_ids=media)

    # Wait until we do this whole thing again
    time.sleep(delay)
