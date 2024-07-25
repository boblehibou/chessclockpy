# SPDX-FileCopyrightText: 2024 Boris Stefanovic <owldev@bluewin.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

from typing import Callable

from chessclock.common import Side, SECOND
from chessclock.config import Action, parse_args
from chessclock.core import Core
from chessclock.themes import Theme, get_theme
from chessclock.ui import Interface


class DefaultInterface(Interface):
	def __init__(self):
		cfg = parse_args()
		self.core = Core(cfg)
		self.actions: dict[Action, Callable] = {
			Action.PRESS_L: (lambda: self.core.press(Side.L)),
			Action.PRESS_R: (lambda: self.core.press(Side.R)),
			Action.ADDTIME_L: (lambda: self.core.add_time(Side.L)),
			Action.ADDTIME_R: (lambda: self.core.add_time(Side.R)),
			Action.PLAY_PAUSE: (lambda: self.core.toggle_run()),
			Action.SWAP_SIDES: (lambda: self.core.swap_sides()),
			Action.RESET: (lambda: self.core.reset()),
		}

	# THEMES

	def get_theme(self) -> Theme | None:
		return get_theme(self.core.config.theme_name)

	# CONFIG

	def get_base_time_ns(self) -> dict[Side, int]:
		return {
			Side.L: self.core.config.time_l * SECOND,
			Side.R: self.core.config.time_r * SECOND,
		}

	def get_increment_ns(self) -> dict[Side, int]:
		return {
			Side.L: self.core.config.increment_l * SECOND,
			Side.R: self.core.config.increment_r * SECOND,
		}

	# GETTERS

	def get_current_times_ns(self) -> dict[Side, int]:
		return self.core.times

	def get_current_side(self) -> Side | None:
		return self.core.side

	def is_running(self) -> bool:
		return self.core.run

	# ACTIONS

	def get_action_map(self) -> dict[Action, Callable[[], None]]:
		return self.actions
