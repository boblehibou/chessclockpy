# SPDX-FileCopyrightText: 2024 Boris Stefanovic <owldev@bluewin.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

from chessclock.common import time_parts


class Theme:
	"""
	A basic theme, to be subclassed.
	Override methods rgb_background, rgb_foreground and rgb_meta.
	They must return iterables of three integers.
	"""

	@classmethod
	def get_theme_name(cls):
		"""
		Get a reasonable default name for any theme based on its class name.
		:return: a reasonable default name for this theme
		"""
		return cls.__name__.lower()

	def get_back_color(self, is_current: bool, is_running: bool, time_left_ns: int) -> tuple[int, int, int, int]:
		"""
		Get opaque background color formatted for use in pyglet.
		There should be no need to override this method.
		:param is_current: True if coloring the active side of the clock
		:param is_running: True if the clock is running, False otherwise
		:param time_left_ns: the time left on the counter, in nanoseconds
		:return: a tuple(r, g, b, a) representation of the color to use for the background of this side of the clock
		"""
		return tuple(list(self.rgb_background(is_current, is_running, time_left_ns)) + [255])

	def get_text_color(self, is_current: bool, is_running: bool, time_left_ns: int) -> tuple[int, int, int, int]:
		"""
		Get opaque text color formatted for use in pyglet.
		There should be no need to override this method.
		:param is_current: True if coloring the active side of the clock
		:param is_running: True if the clock is running, False otherwise
		:param time_left_ns: the time left on the counter, in nanoseconds
		:return: a tuple(r, g, b, a) representation of the color to use for the text of this side of the clock
		"""
		return tuple(list(self.rgb_foreground(is_current, is_running, time_left_ns)) + [255])

	def get_meta_color(self, is_current: bool, is_running: bool, time_left_ns: int) -> tuple[int, int, int, int]:
		"""
		Get opaque color for additional information formatted for use in pyglet.
		There should be no need to override this method.
		:param is_current: True if coloring the active side of the clock
		:param is_running: True if the clock is running, False otherwise
		:param time_left_ns: the time left on the counter, in nanoseconds
		:return: a tuple(r, g, b, a) representation of the color to use for additional information on this side of the clock
		"""
		return tuple(list(self.rgb_meta(is_current, is_running, time_left_ns)) + [255])

	def get_colors(self, is_current: bool, is_running: bool, time_left_ns) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int], tuple[int, int, int, int]]:
		"""
		Convenience method combining the return values of all rgba color methods, each in a format usable by pyglet.
		Do NOT override this method.
		:param is_current: True if coloring the active side of the clock
		:param is_running: True if the clock is running, False otherwise
		:param time_left_ns: the time left on the counter, in nanoseconds
		:return: a tuple((rgba_background), (rgba_foreground), (rgba_meta)), with all elements usable by pyglet
		"""
		return (
			self.get_back_color(is_running, is_current, time_left_ns),
			self.get_text_color(is_running, is_current, time_left_ns),
			self.get_meta_color(is_running, is_current, time_left_ns),
		)

	def rgb_background(self, is_current: bool, is_running: bool, time_left_ns: int) -> tuple[int, int, int]:
		"""
		Get background color for an area.
		:param is_current: True if coloring the active side of the clock
		:param is_running: True if the clock is running, False otherwise
		:param time_left_ns: the time left on the counter, in nanoseconds
		:return: an iterable of three integers : RGB
		"""
		rgb = 0, 48, 0
		if not is_current:
			rgb = 32, 32, 32
		if not is_running:
			rgb = tuple(max(0, e - 16) for e in rgb)
		return rgb

	def rgb_foreground(self, is_current: bool, is_running: bool, time_left_ns: int) -> tuple[int, int, int]:
		"""
		Get foreground/text color for an area.
		:param is_current: True if coloring the active side of the clock
		:param is_running: True if the clock is running, False otherwise
		:param time_left_ns: the time left on the counter, in nanoseconds
		:return: an iterable of three integers : RGB
		"""
		return 0xff, 0xff, 0xff

	def rgb_meta(self, is_current: bool, is_running: bool, time_left_ns: int) -> tuple[int, int, int]:
		"""
		Get color of additional information displayed in an area.
		:param is_current: True if coloring the active side of the clock
		:param is_running: True if the clock is running, False otherwise
		:param time_left_ns: the time left on the counter, in nanoseconds
		:return: an iterable of three integers : RGB
		"""
		return self.rgb_foreground(is_current, is_running, time_left_ns)

	def get_font(self) -> str:
		"""
		Get name of system font to use.
		:return: the name of the system font to use
		"""
		return 'monospace'

	def format_time(self, ns: int) -> str:
		"""
		Get a human readable, displayable string representation for a given time.
		:param ns: time left in nanoseconds
		:return: a string representation of the given time
		"""
		h, m, s, c = time_parts(ns)
		return ''.join([
			f'{h}:' if h != 0 else '',
			f'{m:02d}:' if h != 0 or m != 0 else '',
			f'{s:02d}',
			f'.{c:02d}' if h == 0 and m == 0 else '',
		])

	def format_incr(self, ns: int) -> str:
		"""
		Get a human readable, displayable string representation for a given time increment per turn.
		:param ns: time left in nanoseconds
		:return: a string representation of the given increment
		"""
		h, m, s, c = time_parts(ns)
		return ''.join((
			f'{h}:' if h else '',
			f'{m:02d}:' if h or m else '',
			f'{s:02d}',
			f'.{c:02d}' if c else '',
		))

	def format_time_control(self, t: int = -1, i: int = -1) -> str:
		"""
		Get a human readable, displayable string representation for a given time increment per turn.
		:param t: starting time, in nanoseconds
		:param i: increment per turn, in nanoseconds
		:return: a string representation of the given time control scheme
		"""
		return ' + '.join((
			self.format_time(t),
			self.format_incr(i),
		))
