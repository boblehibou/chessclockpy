from .keymap import Keymap
from .themes import Theme, get_theme


class Config:
	def __init__(
			self,
			*,
			time_seconds: int = 600,  # 10 minutes
			time_l: int = 0,
			time_r: int = 0,
			increment_seconds: int = 0,
			increment_l: int = 0,
			increment_r: int = 0,
			font: str = 'monospace',
			theme: Theme | str | None = None,
			keymap: Keymap | None = None,
	):
		"""
		:param time_seconds: time for both players, in seconds
		:param time_l: time for the player on the left, in seconds; overwrites time_s
		:param time_r: time for the player on the right, in seconds; overwrites time_s
		:param increment_seconds: increment for both players, in seconds
		:param increment_l: increment for the player on the left, in seconds; overwrites increment_s
		:param increment_r: increment for the player on the right, in seconds; overwrites increment_s
		"""
		# params
		if not isinstance(font, str) or not all(map(lambda x: isinstance(x, int), {
			time_seconds, time_l, time_r, increment_seconds, increment_l, increment_r,
		})):
			raise TypeError
		time_seconds = 600 if time_seconds <= 0 else time_seconds
		time_l = time_seconds if time_l <= 0 else time_l
		time_r = time_seconds if time_r <= 0 else time_r
		increment_seconds = 0 if increment_seconds < 0 else increment_seconds
		increment_l = increment_seconds if increment_l < 0 else increment_l
		increment_r = increment_seconds if increment_r < 0 else increment_r
		# themes
		if theme is None:
			theme = Theme()
		elif isinstance(theme, str):
			theme = get_theme(theme.strip())
		elif not isinstance(theme, Theme):
			raise TypeError
		# keymap
		if not keymap:
			keymap = Keymap()
		if not isinstance(keymap, Keymap):
			raise TypeError
		if not keymap.complete:
			print('\nWARNING :\nThe keymap being used is incomplete !\nSome features may be disabled.\n')
		# assign
		self.time_l: int = time_l
		self.time_r: int = time_r
		self.increment_l: int = increment_l
		self.increment_r: int = increment_r
		self.font = font.strip()
		self.theme = theme
		self.keymap = keymap

	def swap_sides(self) -> None:
		"""
		Physically mirrors the configuration.
		This operation only makes sense if the two players have different time controls.
		:return: None
		"""
		self.time_l, self.time_r = self.time_r, self.time_l
		self.increment_l, self.increment_r = self.increment_r, self.increment_l
