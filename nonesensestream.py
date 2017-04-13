import time
import sys
import pprint
import json
import requests

from io import BytesIO

import pprint

from twython import Twython
from PIL import Image
from escpos import printer

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage:\n\tnonesensestream.py hashtag\n\tsans #")
        sys.exit(1)

    hashtags = {}
    for tag in sys.argv[1:]:
        hashtags[tag] = 0

    print(hashtags)

    try: 
        with open('twitter-auth.json') as data_file:    
            auth = json.load(data_file)
    except EnvironmentError: 
        print("twitter-auth.json not found\nget some keys somewhere")
        sys.exit(1)

    #set up the printer
    plt = printer.File("/dev/ulpt0")

    twitter = Twython(app_key=auth["consumer_key"], 
        app_secret=auth["consumer_secret"], 
        oauth_token=auth["access_token_key"], 
        oauth_token_secret=auth["access_token_secret"])

    twitter.verify_credentials()

    print("Following hash tag", end="")
    if len(hashtags) > 1:
        print("s:")
    else
        print(":")

    # Get the most recent tweet with each tag on start up, print nothing
    for tag, since in hashtags.items():
        print("\t#{}".format(tag))
        search = twitter.search(q=tag, count=1)
        tweets = search['statuses']
        hashtags[tag] = tweets[0]['id_str']

    while True:
        time.sleep(15)
        for tag, since in hashtags.items():
            search = twitter.search(q=tag, count=100, since_id=since)
            tweets = search['statuses']

            if len(tweets) == 0:
                print('.', end='', flush=True)
                continue
            else:
                print("")

            hashtags[tag] = tweets[0]['id_str']

            for tweet in tweets:
                print("\t{} {}".format(tweet['user']['screen_name'], tweet['user']['name']))
                print("\t{}".format(tweet['text']))

                plt.text("\t@{}  {}\n".format(tweet['user']['screen_name'], tweet['user']['name']))
                plt.text("\t{}".format(tweet['text']))

                if 'media' in tweet['entities']:
                    media = tweet['entities']['media'][0]
                    imageurl = media['media_url_https']

                    if imageurl.endswith(".jpg"):
                        response = requests.get(imageurl)
                        img = Image.open(BytesIO(response.content))

                        print("\t{}".format(img))
                        ##plt.image(img) #need to figure out how to get the printer to do iamges
                plt.cut()
