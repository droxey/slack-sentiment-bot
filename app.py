# -*- coding: utf-8 -*-
"""
A routing layer for [Slack's Events API](https://api.slack.com/events-api).
"""
import json
import bot
from flask import Flask, request, make_response, render_template

SensiSlackBot = bot.Bot()
slack = SensiSlackBot.client
app = Flask(__name__)


def _event_handler(event_type, slack_event):
    team_id = slack_event["team_id"]

    # TODO: Add event_type logic here.

    message = f"EVENT: {event_type} | {slack_event}"
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def pre_install():
    client_id = SensiSlackBot.oauth["client_id"]
    scope = SensiSlackBot.oauth["scope"]
    return render_template("index.html", client_id=client_id, scope=scope)


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    code_arg = request.args.get('code')
    SensiSlackBot.auth(code_arg)
    return render_template("thanks.html")


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200,
                             {"content_type": "application/json"})

    if SensiSlackBot.verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s \SensiSlackBot has: \
                   %s\n\n" % (slack_event["token"], SensiSlackBot.verification)
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(debug=True)
