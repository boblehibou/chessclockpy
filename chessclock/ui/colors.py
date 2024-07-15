class Theme:
	"""
	A basice theme, to be subclassed.
	Override methods rgb_background and rgb_foreground.
	They must return iterables of three integers.
	"""

	def __init__(self):
		pass

	def get_back_color(self, current: bool, running: bool, time: int):
		return tuple(list(self.rgb_background(current, running, time)) + [255])

	def get_text_color(self, current: bool, running: bool, time: int):
		return tuple(list(self.rgb_foreground(current, running, time)) + [255])

	def get_colors(self, running, current, time):
		return self.rgb_background(running, current, time), self.rgb_foreground(running, current, time)

	def rgb_background(self, current: bool, running: bool, time: int) -> tuple[int, int, int]:
		rgb = 0, 48, 0
		if not current:
			rgb = 32, 32, 32
		if not running:
			rgb = tuple(max(0, e - 16) for e in rgb)
		return rgb

	def rgb_foreground(self, current: bool, running: bool, time: int) -> tuple[int, int, int]:
		return 0xff, 0xff, 0xff
