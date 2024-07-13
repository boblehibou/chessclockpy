from chessclock.config.side import Side, Color


def test_side_opposite():
	for side in Side:
		assert side in {Side.L, Side.R}
		if side is Side.L:
			assert side.opposite == side.R
		if side is Side.R:
			assert side.opposite == side.L


def test_color_opposite():
	for color in Color:
		assert color in {Color.WHITE, Color.BLACK}
		if color is Color.WHITE:
			assert color.opposite == color.BLACK
		if color is Color.BLACK:
			assert color.opposite == color.WHITE
