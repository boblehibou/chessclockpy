# SPDX-FileCopyrightText: 2024 Boris Stefanovic <owldev@bluewin.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

from typing import Callable

from chessclock.config import Action
from chessclock.core import Side
from chessclock.themes import Theme


class Interface:
	"""
	Subclass this class to create a functional binding between user interface and logic.
	It should act as a glue between configuration, logic core, theme engine and user interface.
	"""

	# THEMES

	def get_theme(self) -> Theme | None:
		"""
		Get a theme instance.
		Called in UI constructor if no theme is explicitly provided.
		If this also returns None, then the default theme will be used.
		:return: a theme instance or None
		"""
		return None

	# CONFIG

	def get_base_time_ns(self) -> dict[Side, int]:
		"""
		Get starting time for each player.
		:return: a dictionary mapping each side to its starting time, in nanoseconds
		"""
		raise NotImplementedError

	def get_increment_ns(self) -> dict[Side, int]:
		"""
		Get increment per turn for each player.
		:return: a dictionary mapping each side to its increment per turn, in nanoseconds
		"""
		raise NotImplementedError

	# GETTERS

	def get_current_times_ns(self) -> dict[Side, int]:
		"""
		Get time left for each player.
		:return: a dictionary mapping each side to its increment per turn, in nanoseconds
		"""
		raise NotImplementedError

	def get_current_side(self) -> Side | None:
		"""
		Get the side that is currently counting down.
		:return:
		"""
		raise NotImplementedError

	def is_running(self) -> bool:
		raise NotImplementedError

	# ACTIONS

	def get_action_map(self) -> dict[Action, Callable[[], None]]:
		raise NotImplementedError

	# PROPERTIES and DEFAULT IMPLEMENTATIONS (no need to override)

	def press_L(self) -> None:
		self.get_action_map().get(Action.PRESS_L, lambda: None)()

	def press_R(self) -> None:
		self.get_action_map().get(Action.PRESS_R, lambda: None)()

	def addtime_L(self) -> None:
		self.get_action_map().get(Action.ADDTIME_L, lambda: None)()

	def addtime_R(self) -> None:
		self.get_action_map().get(Action.ADDTIME_R, lambda: None)()

	def play_pause(self) -> None:
		self.get_action_map().get(Action.PLAY_PAUSE, lambda: None)()

	def swap_sides(self) -> None:
		self.get_action_map().get(Action.SWAP_SIDES, lambda: None)()

	def reset(self) -> None:
		self.get_action_map().get(Action.RESET, lambda: None)()

	@property
	def action_map(self) -> dict[Action, Callable[[], None]]:
		return self.get_action_map()
