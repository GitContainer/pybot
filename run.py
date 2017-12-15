import argparse, asyncio, sys # noqa
from bot import Bot # noqa
import constants


def main(args):
	"""Execute bot."""
	batches = args.batches.split(',')
	args.token = constants.BOT_TOKEN
	if args.token is None:
		print('''
token is required, provide them by --token=xxx,
or run --help for further information.
		''')
		return
	lady = Bot(args.token)
	lady = lady.set_questions(constants.QUESTIONS).set_channels(
		batches)
	lady.start()
	lady.send_report(args.hook)


def parse_arguments():
	"""Parse arguments."""
	parser = argparse.ArgumentParser(
		description=constants.BASE_DESCRIPTION,
		epilog=constants.CREATOR)

	parser.add_argument('--batches', type=str, default=constants.DEFAULT_CHANNEL, help='''
		Put in channel name separated by comma(,)
		without spaces.
		''')

	parser.add_argument('--hook', type=str, default=constants.DEFAULT_HOOK, help='''
		Hook endpoint for the standup report to send to.
		''')

	parser.add_argument('--token', type=str, default=None, help='''
		Your bot token.
		''')
	return parser.parse_args()

if __name__ == '__main__':
	args = parse_arguments()
	main(args)
