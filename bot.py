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

# Set up Mastodon if we're not in test mode
if (not testmode):
    from mastodon import Mastodon
    mastodon = Mastodon(
        access_token = 'token.secret',
        api_base_url = 'https://botsin.space/'
    )

# Read in the terminals data and set the initial list
with open(datafile) as f:
    data = json.load(f)
terminals = data.copy()

# Go on forever, picking a random terminal each time around. Remove
# each picked terminal from the list to avoid repeated consecutive
# posts; refill the list when it gets empty (there's a chance of a repeat
# over this refill boundary but that's OK).
while True:

    # Pick a terminal at random and then remove it from the list
    randomchoice = random.randrange(len(terminals))
    terminal = terminals[randomchoice]
    del terminals[randomchoice]

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
