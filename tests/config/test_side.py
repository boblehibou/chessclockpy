from chessclock.core.side import Side


def test_side_opposite():
	for side in Side:
		assert side in {Side.L, Side.R}
		if side is Side.L:
			assert side.opposite == side.R
		if side is Side.R:
			assert side.opposite == side.L
