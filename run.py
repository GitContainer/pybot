from bot import Bot # noqa

BOT_TOKEN = "<your token>"


def main():
	"""Execute bot."""
	lady = Bot(BOT_TOKEN)
	lady = lady.set_question(['A', 'B', 'C']).set_channels(
		['batch1', 'batch2'])
	lady.start()

if __name__ == '__main__':
	main()
