from bot import Bot # noqa

BOT_TOKEN = "xoxb-285783436067-4KKnWM3D98gz4jIlCWZUi6eq"


def main():
	"""Execute bot."""
	lady = Bot(BOT_TOKEN)
	lady = lady.set_question(['A', 'B', 'C']).set_channels(
		['batch1', 'batch2'])
	lady.start()

if __name__ == '__main__':
	main()
