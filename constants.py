"""Constants variables."""


QUESTIONS = [
	'What did you accomplish yesterday?',
	'What are you planning to do today?',
	'Anything standing in your way?'
]

DEFAULT_CHANNEL = 'general'

BOT_TOKEN = 'xoxb-285783436067-4KKnWM3D98gz4jIlCWZUi6eq'

DEFAULT_HOOK = 'localhost:8081/retrieve-standup'

BASE_DESCRIPTION = '''
Lady-bot a python slack standup bot, schedule this script from your system.
Currently running on synchronous manner for each channel,
will be improved later.
'''

CREATOR = 'andy-shi88'

# Perperson question waiting timeout after each question will be reseted
# in seconds
PER_PERSON_TIMEOUT = 180
