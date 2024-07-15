import functools
from time import time_ns

from chessclock.config import Config, Side

from .constants import *
from .format import *


class Core:
	@staticmethod
	def config_to_time(cfg: Config, incr: bool = False) -> dict[Side, int]:
		return {
			Side.L: SECOND * (cfg.increment_l if incr else cfg.time_l),  # in nanoseconds
			Side.R: SECOND * (cfg.increment_r if incr else cfg.time_r),  # in nanoseconds
		}

	def __init__(self, cfg: Config | None = None):
		if cfg is None:
			cfg = Config()
		assert isinstance(cfg, Config)
		# constant
		self.config: Config = cfg
		self.incr: dict[Side, int] = Core.config_to_time(cfg, incr=True)
		# variable
		self._times: dict[Side, int] = Core.config_to_time(self.config)
		self._stamp: int = time_ns()
		self._running: bool = False
		self.side: Side = self.config.starting_side
		self.half_moves: int = 0

	def swap_sides(self):
		if self._running:
			return
		self.incr = {s: self.incr[s.opposite] for s in Side}
		self._times = {s: self._times[s.opposite] for s in Side}
		if self.side in Side:
			self.side = self.side.opposite

	def _update_times(self):
		t = time_ns()
		if self._running:
			self._times[self.side] = max(0, self._times[self.side] + self._stamp - t)
		self._stamp = t

	def reset(self):
		self.half_moves = 0
		self._times = Core.config_to_time(self.config)
		self._running = False
		self.side = self.config.starting_side
		self._update_times()

	@property
	def run(self) -> bool:
		return self._running

	@run.setter
	def run(self, is_start: bool) -> None:
		self._update_times()
		self._running = bool(is_start)

	@property
	def flagged(self) -> dict[Side, bool]:
		self._update_times()
		return {s: self._times[s] <= 0 for s in Side}

	def press(self, pressed_side: Side) -> None:
		"""
		Called when player on `side` side of the clock presses their button.
		:param pressed_side: side relative to the clock of the button being pressed
		:return: True if a switch happened, False otherwise
		"""
		assert pressed_side in Side
		self._update_times()
		if all([
			self._running,
			pressed_side == self.side,
			self._times[self.side] > 0,
		]):
			self._times[self.side] += self.incr[self.side]
			self.half_moves += 1
		self._running = True
		self.side = pressed_side.opposite

	def add_time(self, side: Side | None = None, seconds: int = 15):
		assert isinstance(side, Side) or side is None
		assert isinstance(seconds, int)
		self._update_times()
		if side is None:
			for s in Side:
				self._times[s] += SECOND * seconds
		else:
			self._times[side] += SECOND * seconds

	@property
	def times(self) -> dict[Side, int]:
		self._update_times()
		return self._times.copy()
