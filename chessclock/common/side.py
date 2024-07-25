# SPDX-FileCopyrightText: 2024 Boris Stefanovic <owldev@bluewin.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

from enum import Enum


class Side(Enum):
	"""
	Enum representing to two sides of a chess clock.
	"""

	L = 1
	R = 2

	@property
	def opposite(self):
		"""
		The opposite side of the chess clock.
		:return: the other element of the enum
		"""
		return Side(self.value ^ 0b11)
