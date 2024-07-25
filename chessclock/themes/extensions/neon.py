# SPDX-FileCopyrightText: 2024 Boris Stefanovic <owldev@bluewin.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

import time

from chessclock.themes import Theme


class Neon(Theme):
	"""
	Quick and dirty example theme for testing theme selection from command line and loading.
	"""

	def __init__(self):
		self.begin = 0xB2, 0x0F, 0x3D
		self.end = 0x33, 0xCC, 0x33
		self.period_ns = 5 * 10 ** 9
		self.stamp = time.time_ns()
		self.rise = True
		self.color: tuple[int, int, int] = self.begin

	@property
	def half_period_ns(self):
		return self.period_ns >> 1

	def rgb_background(self, is_current: bool, is_running: bool, time_left_ns: int):
		return super().rgb_background(is_current, is_running, time_left_ns)

	def rgb_foreground(self, is_current: bool, is_running: bool, time_left_ns: int):
		ts = time.time_ns()
		t_diff = ts - self.stamp
		if t_diff > self.half_period_ns:
			t_diff = self.half_period_ns
			self.stamp = ts
			self.rise = False
		if self.rise:
			return tuple(b + ((e - b) * t_diff) // self.half_period_ns for b, e in zip(self.begin, self.end))
		else:
			return tuple(b + ((b - e) * t_diff) // self.half_period_ns for b, e in zip(self.begin, self.end))

	def rgb_meta(self, is_current: bool, is_running: bool, time_left_ns: int):
		return tuple(x ^ 0xff for x in self.rgb_foreground(is_current, is_running, time_left_ns))
