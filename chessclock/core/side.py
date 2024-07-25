from enum import Enum


class Side(Enum):
	L = 1
	R = 2

	@property
	def opposite(self):
		return Side(self.value ^ 0b11)
