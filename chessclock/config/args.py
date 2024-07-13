from argparse import ArgumentParser

from chessclock.config import Side
from chessclock.config.conf import Config

HR: int = 3600
MN: int = 60
SC: int = 1


def parse_time(s: str, incr: bool = False, multiplier: int = 1) -> int:
	"""
	Parses "HH:MM:SS" style string into an integer representing a number of seconds.
	:param s: input string, formatted as "HH:MM:SS"
	:param incr: set to True if interpretation is for increments instead of times
	:param multiplier: multiply the result by this number to get value in time units smaller than a second
	:return: number of seconds represented by this time string
	"""
	if not isinstance(s, str) or not isinstance(multiplier, int):
		raise TypeError
	if not s:
		return 0
	a = [int(v) for v in s.split(':')]
	t = 0
	match len(a):
		case 3:
			t = HR * a[0] + MN * a[1] + SC * a[2]
		case 2:
			t = MN * a[0] + SC * a[1]
		case 1:
			t = SC * a[0] if incr else MN * a[0]
		case _:
			raise ValueError
	return multiplier * t


def parse_side(side: str) -> Side:
	if not isinstance(side, str):
		raise TypeError
	side = side.lower()
	if side in {'l', 'left'}:
		return Side.L
	elif side in {'r', 'right'}:
		return Side.R
	else:
		raise ValueError


def parse_args() -> Config:
	parser = ArgumentParser(
		prog='chessclock',
		description='a simple command-line-configured easy to use (hopefully) chess clock',
	)

	parser.add_argument(
		'-t', '--time',
		default='00:10:00',
		help='time for both players, in following format :  "[HH:]MM:SS" or "MM"',
	)
	parser.add_argument('-l', '--time-l', default='', help='time for clock on the left, defaults to --time')
	parser.add_argument('-r', '--time-r', default='', help='time for clock on the right, defaults to --time')

	parser.add_argument(
		'-T', '--increment',
		default='00:00:00',
		help='increment for both players, in following format :  "[[HH:]MM:]SS"',
	)
	parser.add_argument('-L', '--increment-l', default='', help='time for clock on the left, defaults to --increment')
	parser.add_argument('-R', '--increment-r', default='', help='time for clock on the right, defaults to --increment')

	parser.add_argument(
		'-s', '--starting-side',
		default='L',
		choices={'L', 'R', 'l', 'r', 'LEFT', 'RIGHT', 'left', 'right', 'Left', 'Right'},
		help='the physical location of white (starting) player, relative to the keyboard, or which clock starts counting down first',
	)

	parser.add_argument(
		'-d', '--delayed-start',
		default='',
		help=
		'Do NOT start the clock immediately but let each player play one move before clocks actually start.'
		'A time limit for both of the two half-moves may be set.',
	)

	args = parser.parse_args()
	return Config(
		time_seconds=parse_time(args.time, incr=False),
		time_l=parse_time(args.time_l, incr=False),
		time_r=parse_time(args.time_r, incr=False),
		increment_seconds=parse_time(args.increment, incr=True),
		increment_l=parse_time(args.increment_l, incr=True),
		increment_r=parse_time(args.increment_r, incr=True),
		delayed_start=parse_time(args.delayed_start, incr=True),
		starting_side=parse_side(args.starting_side),
	)
