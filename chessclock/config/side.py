from enum import Enum


class Side(Enum):
	L = 1
	R = 2

	@property
	def opposite(self):
		return Side(self.value ^ 0b11)


class Color(Enum):
	WHITE = 1
	BLACK = 2

	@property
	def opposite(self):
		return Color(self.value ^ 0b11)
