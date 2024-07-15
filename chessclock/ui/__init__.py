import pyglet
from pyglet.window import key

from chessclock.config import Side, parse_args, Config
from chessclock.core import Core, time_to_text, dict_times_to_text

from .colors import Theme


class UI(pyglet.window.Window):
	@staticmethod
	def screen_size():
		display = pyglet.canvas.Display()
		screen = display.get_default_screen()
		return screen.width, screen.height

	def __init__(self, theme: Theme | None = None):
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
		# widgets
		self.back = pyglet.graphics.Batch()
		self.fore = pyglet.graphics.Batch()
		self.times: dict[Side, pyglet.text.Label] = {
			side: pyglet.text.Label(
				text='00:00:00',
				font_name=self.cfg.font,
				font_size=self.scrhei // 10,
				# bold=True,
				stretch=False,
				color=(0xff, 0xff, 0xff, 0xff),
				x=(self.scrwid * (3 if side == Side.R else 1)) // 4,
				y=self.scrhei // 2,
				height=self.scrhei // 7,
				anchor_x='center',
				anchor_y='baseline',
				align='center',
				batch=self.fore,
			) for side in Side
		}
		self.rectangles: dict[Side, pyglet.shapes.Rectangle] = {
			side: pyglet.shapes.Rectangle(
				x=(self.scrwid // 2) * int(side is Side.R),
				y=0,
				width=self.scrwid,
				height=self.scrhei,
				color=(0, 0, 0, 0),
				batch=self.back,
			) for side in Side
		}

	def run(self):
		self.core.reset()
		pyglet.app.run(interval=1 / 30)

	def on_resize(self, w, h):
		super().on_resize(w, h)
		for side in Side:
			self.times[side].x = (w * (3 if side == Side.R else 1)) // 4
			self.times[side].y = h // 2
			self.times[side].height = h // 7
			self.rectangles[side].position = (self.scrwid // 2) * int(side is Side.R), 0
			self.rectangles[side].width, self.rectangles[side].height = self.scrwid, self.scrhei

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
			self.rectangles[side].color = self.theme.get_back_color(current=current, running=running, time=t)
		self.back.draw()
		self.fore.draw()

	def on_key_press(self, symbol, modifiers):
		super().on_key_press(symbol, modifiers)
		match symbol:
			case key.LCTRL:
				self.core.press(Side.L)
			case key.RCTRL:
				self.core.press(Side.R)
			case key.Q:
				self.core.add_time(Side.R)
			case key.P:
				self.core.add_time(Side.L)
			case key.R:
				self.core.reset()
			case key.Z:
				self.core.swap_sides()
			case key.SPACE:
				self.core.run = not self.core.run
			case _:
				pass


if __name__ == '__main__':
	ui = UI()
	ui.run()
