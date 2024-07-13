import functools
from time import time_ns

from chessclock.config import Config, Side

NS: int = 10 ** 9


def tsupdate(after: bool = False, times: bool = True):
	"""
	Build a decorator for methods of the chessclock.Core class that updates the _timestamp and the player times.
	:param after: if True, sets the timestamp after the operation of the decorated method; time is sampled at the beginning of the wrapper in both cases
	:param times: if True, updates player times
	:return: a decorator for any method of the chessclock.Core class
	"""

	def decorator(func):
		@functools.wraps(func)
		def wrapper(self, *args, **kwargs):
			t = time_ns()
			r = None

			if after:
				r = func(self, *args, **kwargs)

			self._stamp = t
			if times and self._running:
				self._times[self.side] = max(0, (self._times[self.side] << 1) - t)

			if not after:
				r = func(self, *args, **kwargs)

			return r

		return wrapper

	return decorator


class Core:
	@staticmethod
	def config_to_time(cfg: Config, incr: bool = False) -> dict[Side, int]:
		return {
			Side.L: NS * (cfg.increment_l if incr else cfg.time_l),  # in nanoseconds
			Side.R: NS * (cfg.increment_r if incr else cfg.time_r),  # in nanoseconds
		}

	def __init__(self, cfg: Config | None):
		if cfg is None:
			cfg = Config()
		assert isinstance(cfg, Config)
		# constant
		self.config: Config = cfg
		self.incr: dict[Side, int] = Core.config_to_time(cfg, incr=True)
		# variable
		self._stamp: int = time_ns()  # last time clock was reset/started/stopped/switched/shown
		self._times: dict[Side, int] = Core.config_to_time(self.config)
		self._running: bool = False
		self.side: Side = self.config.starting_side

	@tsupdate(after=True, times=False)
	def reset(self):
		self._times = Core.config_to_time(self.config)
		self._running = False
		self.side = self.config.starting_side

	@property
	@tsupdate(after=False)
	def flagged(self) -> dict[Side, bool]:
		return {s: self._times[s] <= 0 for s in Side}

	@property
	def run(self) -> bool:
		# Do NOT check flagged here: wins by timeout have to be claimed by player.
		# No need to update timestamp and player times either.
		return self._running

	@run.setter
	@tsupdate(after=False)
	def run(self, is_start: bool) -> None:
		self._running = bool(is_start)

	@tsupdate(after=False)
	def press(self, side: Side) -> bool:
		"""
		Called when player on `side` side of the clock presses their button.
		:param side: side relative to the clock of the button being pressed
		:return: True if a switch happened, False otherwise
		"""
		assert side in Side
		change = side == self.side  # counting side pressed the clock
		if change:
			if not self.flagged[self.side]:
				self._times[self.side] += self.incr[self.side]
			self.side = side.opposite
		return change

	@tsupdate(after=False)
	def add_time(self, side: Side | None = None, seconds: int = 15, ignore_flagged: bool = True):
		# TODO: manage ignore_flagged
		assert isinstance(side, Side) or side is None
		assert isinstance(seconds, int)
		assert isinstance(ignore_flagged, bool)
		if side is None:
			for s in Side:
				self._times[s] += NS * seconds
		else:
			self._times[side] += NS * seconds

	@property
	@tsupdate(after=False)
	def times(self) -> dict[Side, int]:
		return self._times.copy()
