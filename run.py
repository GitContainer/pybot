import logging, argparse, asyncio, sys # noqa
from bot import Bot # noqa
import constants

logging.basicConfig(
	filename="log.txt",
	level=logging.DEBUG,
	format="%(asctime)s:%(levelname)s:%(message)s"
)


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
	lady = Bot(args.token, args.timeout, args.secret)
	lady = lady.set_questions(constants.QUESTIONS).set_channels(
		batches)
	lady.start()
	response = lady.send_report(args.hook)
	logging.info(response)


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

	parser.add_argument('--timeout', type=str, default=constants.PER_PERSON_TIMEOUT, help='''
		Timeout of each member or questions being asked in seconds.
		''')

	parser.add_argument('--secret', type=str, default="", help='''
		Secret string for authenticating to hook.
		''')

	return parser.parse_args()

if __name__ == '__main__':
	args = parse_arguments()
	main(args)
