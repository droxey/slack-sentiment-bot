"""
SentiSlack

GOAL: Perform weekly text/sentiment analysis on slack channel(s).
OUTPUT: Post an anonymized visualization to Twitter, Slack, etc.
DEMONSTRATES:
    Python, Pandas, Matplotlib, Seaborn, APIs, Bots, Heroku
"""
# IMPORTANT: Load matplotlib and disable TKinter to deploy on Heroku.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Any modules that utilize matplotlib (seaborn, etc.) must be imported below.
import json
import os
import time
import numpy as np
import pandas as pd
import requests
import seaborn as sns
import tweepy
import pprint as pp

# Load environment variables.
from dotenv import load_dotenv
load_dotenv('.env')

# Load text analysis libraries.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()


def main():
    auth = tweepy.OAuthHandler(
        os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
    auth.set_access_token(
        os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    print("Bot Initialized!")


if __name__ == "__main__":
    while True:
        main()
        time.sleep(60 * 60)
    print("Received shutdown signal. Goodbye!")
