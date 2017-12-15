"""Question classes to handle lady bot interaction."""


class Question():
	"""Question object to be processed by ladybot."""

	"""Attributes."""
	question_type = None
	question_message = None
	default_response = """
	Sorry, I could not understand your response. I'll record
	it anyway.
	"""

	def __init__(self, question_message="", question_type="free"):
		"""Question intantiation.
		question_type: type of the question [free, conditional]
		"""
		self.question_message = question_message
		self.question_type = question_type

	def set_true_flag(self, flag):
		"""Set true condition for question flag.
		flag: array of expected flag
		"""
		self.true_flag = flag
		return self

	def set_false_flag(self, flag):
		"""Set false condition for question flag.
		flag: array of expected flag
		"""
		self.false_flag = flag
		return self

	def set_false_response(self, response):
		"""Set response of bot to false flag raise.
		response: response of false flag raised
		"""
		self.false_response = response
		return self

	def get_response(self, answer):
		"""Get response of anwer.
		answer: answer gotten by bot
		"""
		if self.question_type == "free":
			pass
		if answer in self.true_flag:
			return self.true_response
		elif answer in self.false_flag:
			return self.false_response
		else:
			return self.default_response
