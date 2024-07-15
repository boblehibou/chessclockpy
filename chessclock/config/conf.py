from .side import Side


class Config:
	NO_DELAY: int = 0
	INFINITE_DELAY: int = -1

	def __init__(
			self,
			time_seconds: int = 600,  # 10 minutes
			time_l: int = 0,
			time_r: int = 0,
			increment_seconds: int = 0,
			increment_l: int = 0,
			increment_r: int = 0,
			delayed_start: int = 0,
			starting_side: Side = Side.L,
			font: str = 'monospace',
	):
		"""
		:param time_seconds: time for both players, in seconds
		:param time_l: time for the player on the left, in seconds; overwrites time_s
		:param time_r: time for the player on the right, in seconds; overwrites time_s
		:param increment_seconds: increment for both players, in seconds
		:param increment_l: increment for the player on the left, in seconds; overwrites increment_s
		:param increment_r: increment for the player on the right, in seconds; overwrites increment_s
		:param delayed_start: time in seconds for first move, without clock countdown (like chess.com); 0 => no_delay , -1 => infinite
		:param starting_side: side on which the clock first starts counting down
		"""
		# assign
		self.time_seconds: int = time_seconds
		self.time_l: int = time_l
		self.time_r: int = time_r
		self.increment_seconds: int = increment_seconds
		self.increment_l: int = increment_l
		self.increment_r: int = increment_r
		self.delayed_start: int = delayed_start
		self.starting_side: Side = starting_side
		assert isinstance(font, str)
		self.font = font.strip()
		# type
		if not (isinstance(self.starting_side, Side) and self.starting_side in Side) or not all([
			isinstance(x, int) for x in [
				self.time_seconds, self.time_l, self.time_r,
				self.increment_seconds, self.increment_l, self.increment_r,
				self.delayed_start,
			]
		]):
			raise TypeError
		# value
		if self.delayed_start < -1 or any([
			x < 0 for x in [
				self.time_seconds, self.time_l, self.time_r,
				self.increment_seconds, self.increment_l, self.increment_r,
			]
		]):
			raise ValueError
		# time
		if not self.time_l:
			self.time_l = self.time_seconds
		if not self.time_r:
			self.time_r = self.time_seconds
		if not (self.time_l > 0 and self.time_r > 0):
			raise ValueError('time not set for at least one of the players')
		# increment
		if not self.increment_l:
			self.increment_l = self.increment_seconds
		if not self.increment_r:
			self.increment_r = self.increment_seconds
