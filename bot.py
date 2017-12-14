import time # noqa
from datetime import timedelta, datetime
from slackclient import SlackClient


class Bot(object):
    """Slack bot class."""

    """Attributes."""
    token = None
    channels = []
    reports = []
    client = None
    login_data = None
    end_time = None

    def __init__(self, token):
        """Initialize bot instance.
        token: slack bot authorization token
        """
        self.token = token

    def start(self):
        """Boot up slack bot."""
        self.client = SlackClient(self.token)
        if self.client.rtm_connect():
            self.login_data = self.client.get_login_data()
            print("bot running")
            for channel in self.get_all_channels():
                if channel['name'] in self.channels:
                    self.reports.append(self.standup_start(channel['id']))
            print(self.reports)

    def set_channels(self, channels):
        """Pass list of channel to execute standup.
        :channels array of channels
        """
        self.channels = channels
        return self

    def set_timeframe(self, interval=7200):
        """Set slackbot existence timeframe.
        :time, time in seconds. Default to 1 hours
        """
        self.end_time = datetime.now() + timedelta(seconds=time)
        return self

    def greet(self, channel):
        """Initial greeting.
        channel: target channel name
        """
        self.client.rtm_send_message(channel, "Hello, We'll start the stand up \
            soon.")

    def farewell(self, channel):
        """Sum up the standups.
        channel: target channel name
        """
        self.client.rtm_send_message(channel, "That's it for today \
            Thanks for your effort today")

    def standup_start(self, channel):
        """Start stand up on channel.
        channel: respective channel
        """
        report = {}
        report['channel'] = channel
        report['members'] = {}
        self.greet(channel)
        members = self.get_members(channel)

        for member in members:
            if member == self.login_data['id']:
                continue
            # prepare data
            report['members'] = []
            data = {}
            data['id'] = member
            ongoing = True
            count = -1
            # bot start
            self.client.rtm_send_message(channel, "Hello <@{}> type `start` \
                to begin, or `skip` if you want to skip for \
                today.".format(member))
            member_time_out = datetime.now() + timedelta(seconds=20)
            while ongoing:
                if datetime.now() > member_time_out:
                    data['message'] = None
                    self.client.rtm_send_message(channel, "<@{}> is not available \
                        Let's move to another member.".format(member))
                    break
                for slack_message in self.client.rtm_read():

                    message = slack_message.get("text")
                    user = slack_message.get("user")
                    from_channel = slack_message.get("channel")
                    # Conditional to make sure reply come from right
                    # member and channel
                    if not message or not user or user == self.login_data['id']:
                        continue
                    if from_channel != channel or user != member:
                        continue
                    if message == 'skip':
                        data['message'] = None
                        self.client.rtm_send_message(
                            from_channel, 'okay')
                        ongoing = False
                        break
                    count += 1
                    data['q_' + str(count)] = message
                    if count >= len(self.questions):
                        ongoing = False
                        break
                    self.client.rtm_send_message(
                        from_channel, self.questions[count])
            self.client.rtm_send_message(
                from_channel, "Thanks <@{}>.".format(member))
            report['members'].append(data)

        self.farewell(channel)
        return report

    def get_all_channels(self):
        """Get all channel associated with current bot."""
        response = self.client.api_call("channels.list")
        return response['channels']

    def get_members(self, channel):
        """Get members of channel.
        channel: channel name
        """
        response = self.client.api_call("channels.info", channel=channel)
        return response['channel']['members']

    def set_question(self, questions):
        """Set question to be asked.
        questions: array of questions
        """
        self.questions = questions
        return self
