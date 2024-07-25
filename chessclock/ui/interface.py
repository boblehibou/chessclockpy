from typing import Callable

from chessclock.config import Action
from chessclock.core import Side


class Interface:

	# GETTERS

	def get_base_time_ns(self) -> dict[Side, int]:
		raise NotImplementedError

	def get_increment_ns(self) -> dict[Side, int]:
		raise NotImplementedError

	def get_current_times_ns(self) -> dict[Side, int]:
		raise NotImplementedError

	def get_current_side(self) -> Side | None:
		raise NotImplementedError

	def is_running(self) -> bool:
		raise NotImplementedError

	# ACTIONS

	def get_action_map(self) -> dict[Action, Callable[[], None]]:
		raise NotImplementedError

	@property
	def action_map(self) -> dict[Action, Callable[[], None]]:
		return self.get_action_map()

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
