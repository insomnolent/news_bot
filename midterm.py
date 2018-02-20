# twitter bot is called @thisisnot_a_bot

import tweepy
import random
import sys
import csv
import os
import time

# Consumer keys and access tokens, used for OAuth
consumer_key = '2SPYgSLXVonbC0hxSNtBdGjER'
consumer_secret = 'JWIvsCAz0hxB6UU9VdjNPVjEAzijfMmXy5nJcr1btQwvWEdXvM'
access_token = '963204658306080768-eKkkTWuYzH8BBddHExVQKRLKVaqDLqg'
access_token_secret = '1QzywUT5XvwZH1lVByZeyOWpMi3fTmyF6htJBJlwckQU7'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# Fix for an encoding error. Basically Twitter allows characters that IDLE can't print out, so
# you have to remove the characters that lie outside of this range.
#
# Whenever you want to print text, use .translate(non_bmp_map) on the end.
# e.g. str(myVar).translate(non_bmp_map)
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# a set holding all of the links you tweet
all_news = set()
# a set holding all unique replies you give
all_replies = set()


# only sends tweet 40% of the time
def send_tweet():
    x = random.randint(1,5)
    if x <= 2:
        return True
    else:
        return False


def compose_tweet(handle, tweet_number):
    tweet = "Hello @%s!" % (handle)
    tweet += " You are user number %s that I am replying to!" % (str(tweet_number))

    # if there aren't any news articles in all_news yet - just in case tweet_news() changes later
    # and you want to reply to users before posting any articles yet?
    if len(all_news) == 0:
        # then just tweet a default article until next loop adds more news to the all_news set
        latest_news = "https://www.engadget.com/2018/02/15/crispr-detect-hpv-and-zika/"
    else:
        # else, take a random article that you just added to the all_news set
        random_article = random.randint(0, len(all_news) - 1)
        latest_news = list(all_news)[random_article]
    # add article link for user to check out
    tweet += " Check out this latest article: " + latest_news
    return tweet


# reply to someone who tweets at you
def reply_to_someone(tweet_number):
    # search for all tweets that reference the bot
    other_tweets = api.search(q="@thisisnot_a_bot")

    for t in other_tweets:
        tweet_id = t.id
        handle = t.user.screen_name
        # to check if you have responded to this tweet ID before
        if tweet_id not in all_replies:
            tweet = compose_tweet(handle, tweet_number)
            all_replies.add(tweet_id)
            tweet_number += 1
            print "Responding to tweet with: " + tweet
            api.update_status(tweet, t.id)
            # pauses 30 seconds between each response to different tweets
            time.sleep(15)
        else:
            print "Could not respond to tweet because of duplicate text"

    # return tweet_number to keep track of your responses
    return tweet_number


# to start posting articles and responding to other users
def tweet_news():
    os.chdir('/Users/christinesun/PycharmProjects/DH150/midterm')
    # read in CSV file
    data = open('news_articles.csv')
    news = csv.reader(data)

    # keeps track of tweets you reply to users with
    # since it replies with something like "You are user number <track_tweet>" to avoid duplicates
    track_tweet = 1

    # be able to both reply to tweets and also tweet articles while looping through each row of CSV
    # the CSV file is a bit large so this way the bot will be able to respond to other twitter accounts for longer time
    for x in news:
        # check if you can send a tweet or not - only 40% chance so this way it seems random
        # keeps going through while loop and waiting 5 minutes after each iteration
        # so it will still send that link eventually but at random times through day
        while send_tweet() is False:
            print "Unable to send tweet for link: " + x[0]
            time.sleep(10)
        # if sending tweet is allowed (i.e. if send_tweet returns true)
        if send_tweet():
            if ("https://" or "http://") in x[0]:
                # check if tweet has been sent before
                if x[0] not in all_news:
                    all_news.add(x[0])
                    print "Tweeting this link: " + x[0]
                    api.update_status(x[1] + ": " + x[0])

        # reply to people who send me a Tweet
        # I guess this also kind of simulates a user who would tweet something and also
        # scroll through their twitter feed afterwards and reply to people
        new_num = reply_to_someone(track_tweet)
        track_tweet = new_num

        # can decrease this number later for testing purposes
        time.sleep(10)

    # when all tweets and links in CSV file are sent
    data.close()


# deletes all previous tweets just for testing purposes
def delete_all():
    print "Is it ok to delete all tweets? Type YES to confirm."
    do_delete = raw_input("> ")
    if do_delete.upper() == 'YES':
        for text in tweepy.Cursor(api.user_timeline).items():
            try:
                api.destroy_status(text.id)
                print "Deleted:", text.id
            except:
                print "Failed to delete:", text.id


if __name__ == "__main__":
    ### to delete all tweets for testing purposes
    ### make sure to run this function before tweet_news() so there aren't duplicate tweet errors
    # delete_all()

    tweet_news()
