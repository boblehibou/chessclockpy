# SPDX-FileCopyrightText: 2024 Boris Stefanovic <owldev@bluewin.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

import pyglet

from chessclock.config.keymap import Keymap
from chessclock.themes import Theme, get_theme
from chessclock.core import Side
from .interface import Interface


class UI(pyglet.window.Window):
	"""
	The user interface for the chess clock.
	"""

	@staticmethod
	def screen_size():
		"""
		Get the size of the screen, in pixels.
		:return: a tuple describing the size of the screen, in pixels, in format (width,height)
		"""
		display = pyglet.canvas.Display()
		screen = display.get_default_screen()
		return screen.width, screen.height

	def __init__(
			self,
			interface_instance: Interface,
			key_bindings: Keymap | None = None,
			theme: Theme | None = None,
	):
		"""
		UI constructor.
		:param interface_instance: an Interface instance
		:param key_bindings: a complete Keymap instance
		:param theme: a Theme instance
		"""
		super().__init__()
		# interface
		if not isinstance(interface_instance, Interface):
			raise TypeError
		self.interface: Interface = interface_instance
		# keymap
		if key_bindings is None:
			key_bindings = Keymap()
		if not isinstance(key_bindings, Keymap):
			raise TypeError
		self.keymap = key_bindings
		# theme
		if theme is None:
			theme = self.interface.get_theme()
		if theme is None:
			theme = Theme()
		if isinstance(theme, str):
			theme = get_theme(theme)
		if not isinstance(theme, Theme):
			raise TypeError
		self.theme = theme
		# fullscreen
		self.scrwid, self.scrhei = UI.screen_size()
		self.width = self.scrwid
		self.height = self.scrhei
		self.set_fullscreen(fullscreen=True, width=self.scrwid, height=self.scrhei)
		self.set_mouse_visible(False)
		# widgets
		self.back = pyglet.graphics.Batch()
		self.fore = pyglet.graphics.Batch()
		self.meta = pyglet.graphics.Batch()
		self.areas: dict[Side, pyglet.shapes.Rectangle] = {
			side: pyglet.shapes.Rectangle(
				x=(self.scrwid // 2) * int(side is Side.R),
				y=0,
				width=self.scrwid,
				height=self.scrhei,
				batch=self.back,
			) for side in Side
		}
		self.times: dict[Side, pyglet.text.Label] = {
			side: pyglet.text.Label(
				text='00:00:00',
				font_name=self.theme.get_font(),
				anchor_x='center',
				anchor_y='baseline',
				align='center',
				batch=self.fore,
			) for side in Side
		}
		self.description: dict[Side, pyglet.text.Label] = {
			side: pyglet.text.Label(
				text=self.theme.format_time_control(
					self.interface.get_base_time_ns()[side],
					self.interface.get_increment_ns()[side],
				),
				font_name=self.theme.get_font(),
				anchor_x='center',
				anchor_y='baseline',
				align='center',
				batch=self.meta,
			) for side in Side
		}

	def run(self, interval: float = 1 / 30) -> None:
		"""
		Starts the application.
		:param interval: the update interval / "framerate"
		:return: None
		"""
		self.interface.reset()
		pyglet.app.run(interval=interval)

	def on_resize(self, w, h):
		super().on_resize(w, h)
		for side in Side:
			self.areas[side].position = (self.scrwid // 2) * int(side is Side.R), 0
			self.areas[side].width, self.areas[side].height = self.scrwid, self.scrhei
			self.times[side].x = (w * (3 if side == Side.R else 1)) // 4
			self.times[side].y = h // 2
			self.times[side].font_size = h // 10
			self.description[side].x = (w * (3 if side == Side.R else 1)) // 4
			self.description[side].y = h * 5 // 6
			self.description[side].font_size = h // 30

	def on_draw(self):
		times = self.interface.get_current_times_ns()
		texts = {s: self.theme.format_time(t) for s, t in times.items()}
		is_running = self.interface.is_running()
		self.clear()
		for side in Side:
			is_current = side == self.interface.get_current_side()
			t = times[side]
			self.times[side].text = texts[side]
			self.times[side].color = self.theme.get_text_color(is_current=is_current, is_running=is_running, time_left_ns=t)
			self.areas[side].color = self.theme.get_back_color(is_current=is_current, is_running=is_running, time_left_ns=t)
		self.back.draw()
		self.fore.draw()
		if not is_running:
			base, incr = self.interface.get_base_time_ns(), self.interface.get_increment_ns()
			for side in Side:
				self.description[side].text = self.theme.format_time_control(base[side], incr[side])
				self.description[side].color = self.theme.get_meta_color(
					is_current=(side == self.interface.get_current_side()),
					is_running=is_running,
					time_left_ns=times[side],
				)
			self.meta.draw()

	def on_key_press(self, symbol, modifiers):
		super().on_key_press(symbol, modifiers)
		action = self.keymap.get(symbol)
		self.interface.action_map.get(action, lambda: None)()
