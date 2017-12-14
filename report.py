"""Report class for wrapping up all standup response."""


class Report(object):
	"""Report will consist of following format.
	report: array
		channel: string
		members: array
			message: string
	"""

	def __init__(self):
		"""Instantiate report object."""
		self.report = []
		self.channel_report = {}
		self.member_report = []

	def push_member_report(self):
		"""Push member wrap up report."""
		pass

	def push_channel_report(self):
		"""Push channel wrap up report."""
		pass

	def deserialize(self):
		"""Deserialize report object as json."""
		pass
