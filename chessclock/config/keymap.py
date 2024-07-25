# SPDX-FileCopyrightText: 2024 Boris Stefanovic <owldev@bluewin.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

from enum import Enum, auto

from pyglet.window import key


class Action(Enum):
	"""
	An enumeration of all possible user interactions.
	If this were a physical chess clock, every action would be a button.
	"""
	PRESS_L = auto()
	PRESS_R = auto()
	ADDTIME_L = auto()
	ADDTIME_R = auto()
	PLAY_PAUSE = auto()
	SWAP_SIDES = auto()
	RESET = auto()


class Keymap:
	"""
	A mapping of keyboard keys to chess clock actions.
	"""

	def __init__(
			self,
			use_numpad_for_right: bool = False,
			*,
			key_press_l: int = key.LCTRL,
			key_press_r: int = key.RCTRL,
			key_addtime_l: int = key.P,
			key_addtime_r: int = key.Q,
			key_play_pause: int = key.SPACE,
			key_swap_sides: int = key.Z,
			key_reset: int = key.R,
	):
		"""
		Keymap constructor.
		:param use_numpad_for_right: convenience parameter used to move right side's controls to numpad
		:param key_press_l: key used to end left side's turn
		:param key_press_r: key used to end right side's turn
		:param key_addtime_l: key used to add time to left side
		:param key_addtime_r: key used to add time to right side
		:param key_play_pause: key used to pause and resume clock countdown
		:param key_swap_sides: key used to physically swap the time controls and times left between players
		:param key_reset: key used to set the clock to its starting state, ready to begin a new game
		"""
		if use_numpad_for_right:
			key_press_r = key.NUM_ENTER
			key_addtime_l = key.NUM_9
		keys = [key_press_l, key_press_r, key_addtime_l, key_addtime_r, key_play_pause, key_swap_sides, key_reset]
		acts = [Action.PRESS_L, Action.PRESS_R, Action.ADDTIME_L, Action.ADDTIME_R, Action.PLAY_PAUSE, Action.SWAP_SIDES, Action.RESET]
		if not len(set(keys)) == len(keys):
			raise KeyError
		self.bindings: dict[int, Action] = {keys[i]: acts[i] for i in range(len(keys))}

	def remap(self, newkey: int, action: Action) -> bool:
		"""
		Bind a key to an action, overwriting previous bindings if there is a conflict.
		Multiple keys may be bound to the same action.
		:param newkey: key to bind
		:param action: action bound to the key
		:return: True if the resulting keymap covers all functionality, False otherwise
		"""
		assert isinstance(newkey, int)
		assert action in Action
		self.bindings[newkey] = action
		return self.complete

	@property
	def complete(self) -> bool:
		"""
		If returned value is True, there is a keybinding for every possible user action.
		:return: True if every user action has at least one key bound to it, False otherwise
		"""
		for a in Action:
			if a not in self.bindings.values():
				return False
		return True

	def get(self, symbol: int) -> Action | None:
		return self.bindings.get(symbol, None)
