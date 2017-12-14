import time, json # noqa
from datetime import timedelta, datetime
from slackclient import SlackClient


class Bot(object):
    """Slack bot class.
    Handle all basic greeting to member rolling standup, including
    timeframe of each standup.
    """

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

    def is_bot(self, member):
        """Check if member is current bot.
        member: specified member id
        """
        return self.login_data['id'] == member

    def extract_slack_message(self, message):
        """Extract slack message body.
        message: response from slack
        """
        text, user, channel = message.get(
            'text'), message.get(
            'user'), message.get('channel')
        if not text or not user or not channel or user == self.login_data['id']:
            return None
        return {'user': user, 'text': text, 'channel': channel}

    def exec_member(self, member, channel):
        """Loop through every questions, and pass to user.
        member: interacted member.
        """
        ongoing = True
        count = -1
        data = {}
        # bot start
        self.client.rtm_send_message(channel, """
            Hello <@{}> type `start` to begin,\
            or `skip` if you want to skip for \
            today.
            """.format(member))
        member_time_out = datetime.now() + timedelta(seconds=20)
        while ongoing:
            if datetime.now() > member_time_out:
                data['message'] = "timeout"
                self.client.rtm_send_message(channel, "<@{}> is not available \
                    Let's move to another member.".format(member))
                break
            for slack_message in self.client.rtm_read():

                message = self.extract_slack_message(slack_message)
                if message is None:
                    continue
                if message['channel'] != channel or message['user'] != member:
                    continue
                if message['text'].lower() == 'skip':
                    data['message'] = "skipped"
                    self.client.rtm_send_message(
                        message['channel'], 'okay')
                    ongoing = False
                    break
                count += 1
                data['q_' + str(count)] = message['text']
                if count >= len(self.questions):
                    ongoing = False
                    break
                self.client.rtm_send_message(
                    message['channel'], self.questions[count])
        self.client.rtm_send_message(
            message['channel'], "Thanks <@{}>.".format(member))
        return data

    def standup_start(self, channel):
        """Start stand up on channel.
        channel: respective channel
        TODO: breakdown this method
        """
        report = {}
        report['channel'] = channel
        report['members'] = []
        self.greet(channel)
        members = self.get_members(channel)

        for member in members:
            if self.is_bot(member):
                continue
            report['members'].append(
                self.exec_member(member, channel))
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

    def set_questions(self, questions):
        """Set question to be asked.
        questions: array of questions
        """
        self.questions = questions
        return self

    def push_question(self, question):
        """Push question to queue.
        question: Question object to be pushed.
        """
        self.questions.append(question)
        return self

    def send_report(self, hook):
        """Send report to hook.
        hook: endpoint to receive the report
        """
        payload = json.dumps(self.reports)
        print('sending to %s', hook)
        print(payload)
