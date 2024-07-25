# SPDX-FileCopyrightText: 2024 Boris Stefanovic <owldev@bluewin.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

from time import time_ns

from chessclock.config import Config
from chessclock.common.constants import *
from chessclock.common.side import Side


class Core:
	"""
	Class defining the core functionality of the clock.
	"""

	@staticmethod
	def config_to_time(cfg: Config, incr: bool = False) -> dict[Side, int]:
		"""
		Map each side of the clock to its configured starting time or increment.
		:param cfg: the clock configuration
		:param incr: if True, map sides to increments rather than starting times
		:return: a dictionary mapping each side to its starting time or increment (depending on incr parameter)
		"""
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
		self.incr: dict[Side, int] = Core.config_to_time(self.config, incr=True)
		# variable
		self._running: bool = False
		self._times: dict[Side, int] = Core.config_to_time(self.config)
		self.side: Side | None = None
		self.half_moves: int = 0
		self._stamp: int = time_ns()

	def _update_times(self) -> None:
		"""
		Update the timers.
		Use this method before returning any value to code residing outside of this class.
		This method should only be called from inside this class.
		:return: None
		"""
		t = time_ns()
		if self._running and self.side in Side:
			self._times[self.side] = max(0, self._times[self.side] + self._stamp - t)
		self._stamp = t

	@property
	def times(self) -> dict[Side, int]:
		"""
		Get time left for each side.
		:return: a dictionary mapping each side to the time it has left until flagging
		"""
		self._update_times()
		return self._times.copy()

	@property
	def describe(self) -> dict[Side, tuple[int, int]]:
		"""
		Describe each side's state.
		:return: a dictionary mapping each side to a tuple composed of time left and increment per turn
		"""
		return {s: (self._times[s], self.incr[s]) for s in Side}

	@property
	def flagged(self) -> dict[Side, bool]:
		"""
		Get flagged state for both players.
		:return: a dictionary mapping each player to a boolean indicating whether they have flagged or not
		"""
		self._update_times()
		return {s: self._times[s] <= 0 for s in Side}

	@property
	def run(self) -> bool:
		"""
		Whether the clock is running or not.
		:return: True if the clock is running, False otherwise
		"""
		return self._running and self.side in Side

	@run.setter
	def run(self, is_start: bool) -> None:
		"""
		Set the running state of the clock.
		:param is_start: set to True if clock is to run; set to False otherwise
		:return: None
		"""
		self._update_times()
		self._running = bool(is_start) and self.side in Side

	def reset(self) -> None:
		"""
		Place the clock in a state in which it is set and ready for a new game,
		using the same configuration.
		:return:
		"""
		self._running = False
		self._times = Core.config_to_time(self.config)
		self.side = None
		self.half_moves = 0
		self._update_times()

	def swap_sides(self) -> bool:
		"""
		Swaps all aspects of the clock between sides.
		:return:
		"""
		if self._running:
			return False
		self.incr = {s: self.incr[s.opposite] for s in Side}
		self._times = {s: self._times[s.opposite] for s in Side}
		if self.side in Side:
			self.side = self.side.opposite
		return True

	def toggle_run(self) -> None:
		"""
		Pause and resume clock countdown.
		:return: None
		"""
		self.run = not self.run

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
			self._times.get(self.side, 0) > 0,
		]):
			self._times[self.side] += self.incr[self.side]
			self.half_moves += 1
		self._running = True
		self.side = pressed_side.opposite

	def add_time(self, player: Side | None = None, seconds: int = 15) -> None:
		"""
		Add time to the opponent's clock (inspired by chess.com).
		Can be useful when a disturbance occurred or one wishes to prolong the match.
		:param player: side to which time is to be added; if None, adds time to both sides
		:param seconds: time to add to the clock(s), in seconds
		:return: None
		"""
		assert isinstance(player, Side) or player is None
		assert isinstance(seconds, int)
		self._update_times()
		if player is None:
			for s in Side:
				self._times[s] += SECOND * seconds
		else:
			self._times[player] += SECOND * seconds
