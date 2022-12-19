#!/usr/bin/env python3

# Terminal bot - post a random terminal status, based on the info in 
# the wonderful Terminal Wiki. This work is a remix of that, also under
# the same licence, i.e. CC BY-SA 3.0).

import random
import json
import sys

datafile = './terminals.json'
testmode = "--test" in sys.argv


# Set up Mastodon if we're not in test mode
if (not testmode):
    from mastodon import Mastodon
    mastodon = Mastodon(
        access_token = 'token.secret',
        api_base_url = 'https://botsin.space/'
    )

with open(datafile) as f:
    data = json.load(f)

    # Pick a terminal at random
    terminal = data[random.randrange(len(data))]

    # Main title is the make and model
    title = " ".join([terminal["make"], terminal["model"]])

    # We'll pick a random entry from the terminal's list of attributes
    attributes = list(terminal["attributes"])
    attribute_key = attributes[random.randrange(len(attributes))]
    attribute_val = terminal["attributes"][attribute_key]

    # Compose the status text, including attribution
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
