from typing import Callable

import pyglet

from chessclock.config import Config, parse_args
from chessclock.core import Core, dict_times_to_text, Side, time_control_to_text, SECOND
from chessclock.config.keymap import Action, Keymap
from chessclock.config.themes import Theme


class UI(pyglet.window.Window):
	@staticmethod
	def screen_size():
		"""
		Get the screen size, in pixels.
		:return: a tuple describing the size of the screen, in pixels, in format (width,height)
		"""
		display = pyglet.canvas.Display()
		screen = display.get_default_screen()
		return screen.width, screen.height

	def __init__(self, *, key_bindings: Keymap | None = None, theme: Theme | None = None):
		super().__init__()
		# logic
		self.cfg: Config = parse_args()
		self.core: Core = Core(self.cfg)
		# theme
		self.theme = theme if isinstance(theme, Theme) else Theme()
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
				font_name=self.cfg.font,
				anchor_x='center',
				anchor_y='baseline',
				align='center',
				batch=self.fore,
			) for side in Side
		}
		self.description: dict[Side, pyglet.text.Label] = {
			side: pyglet.text.Label(
				text=time_control_to_text(
					SECOND * {Side.L: self.cfg.time_l, Side.R: self.cfg.time_r}[side],
					SECOND * {Side.L: self.cfg.increment_l, Side.R: self.cfg.increment_r}[side],
				),
				font_name=self.cfg.font,
				anchor_x='center',
				anchor_y='baseline',
				align='center',
				batch=self.meta,
			) for side in Side
		}
		# controls
		self.keymap: Keymap = key_bindings if key_bindings else Keymap()
		if not self.keymap.complete:
			raise KeyError

		def play_pause():
			self.core.run = not self.core.run

		def swap_sides():
			if self.core.swap_sides():
				self.cfg.swap_sides()

		self.action_map: dict[Action, Callable] = {
			Action.PRESS_L: lambda: self.core.press(Side.L),
			Action.PRESS_R: lambda: self.core.press(Side.R),
			Action.ADDTIME_L: lambda: self.core.add_time(Side.L),
			Action.ADDTIME_R: lambda: self.core.add_time(Side.R),
			Action.PLAY_PAUSE: play_pause,
			Action.SWAP_SIDES: swap_sides,
			Action.RESET: lambda: self.core.reset(),
		}

	def run(self, interval: float = 1 / 30) -> None:
		"""
		Starts the application.
		:param interval: the update interval / "framerate"
		:return: None
		"""
		self.core.reset()
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
		times = self.core.times
		texts = dict_times_to_text(times)
		self.clear()
		running = self.core.run
		for side in Side:
			current = side == self.core.side
			t = times[side]
			self.times[side].text = texts[side]
			self.times[side].color = self.theme.get_text_color(current=current, running=running, time=t)
			self.areas[side].color = self.theme.get_back_color(current=current, running=running, time=t)
		self.back.draw()
		self.fore.draw()
		if not self.core.run:
			for side in Side:
				self.description[side].text = time_control_to_text(
					SECOND * {Side.L: self.cfg.time_l, Side.R: self.cfg.time_r}[side],
					SECOND * {Side.L: self.cfg.increment_l, Side.R: self.cfg.increment_r}[side],
				)
			self.meta.draw()

	def on_key_press(self, symbol, modifiers):
		super().on_key_press(symbol, modifiers)
		action = self.keymap.bindings.get(symbol, None)
		callback = self.action_map.get(action, lambda: None)
		callback()
