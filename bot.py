# -*- coding: utf-8 -*-
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

# Slack wrapper.
from slackclient import SlackClient

# Load environment variables.
from dotenv import load_dotenv
load_dotenv('.env')

# Load text analysis libraries.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

authed_teams = {}


class Bot(object):
    """ Instanciates a Bot object to handle Slack onboarding interactions."""

    def __init__(self):
        super(Bot, self).__init__()
        self.name = "SentiSlack"
        self.emoji = ":robot_face:"
        self.oauth = {
            "client_id": os.environ.get("SLACK_CLIENT_ID"),
            "client_secret": os.environ.get("SLACK_CLIENT_SECRET"),
            "scope": "bot"
        }
        self.verification = os.environ.get("SLACK_VERIFICATION_TOKEN")
        self.client = SlackClient("")
        self.messages = {}

        auth = tweepy.OAuthHandler(
            os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
        auth.set_access_token(
            os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
        self.tweepy_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
        print("Bot Initialized!")

    def auth(self, code):
        auth_response = self.client.api_call(
            "oauth.access",
            client_id=self.oauth["client_id"],
            client_secret=self.oauth["client_secret"],
            code=code)
        team_id = auth_response["team_id"]
        authed_teams[team_id] = {
            "bot_token": auth_response["bot"]["bot_access_token"]
        }
        self.client = SlackClient(authed_teams[team_id]["bot_token"])
