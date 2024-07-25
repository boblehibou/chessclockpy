from argparse import ArgumentParser

from .conf import Config


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
	hr: int = 3600
	mn: int = 60
	sc: int = 1
	a = [int(v) for v in s.split(':')]
	t = 0
	match len(a):
		case 3:
			t = hr * a[0] + mn * a[1] + sc * a[2]
		case 2:
			t = mn * a[0] + sc * a[1]
		case 1:
			t = sc * a[0] if incr else mn * a[0]
		case _:
			raise ValueError
	return multiplier * t


def parse_args() -> Config:
	parser = ArgumentParser(
		prog='chessclock',
		description='simple chess clock configured on the command line',
	)

	parser.add_argument(
		'-t', '--time',
		default='00:10:00',
		help='time for both players; format :  "[HH:]MM:SS" or "MM"',
	)
	parser.add_argument('-l', '--time-l', default='', help='time for clock on the left, defaults to --time')
	parser.add_argument('-r', '--time-r', default='', help='time for clock on the right, defaults to --time')

	parser.add_argument(
		'-T', '--increment',
		default='00:00:00',
		help='increment for both players; format :  "[[HH:]MM:]SS"',
	)
	parser.add_argument('-L', '--increment-l', default='', help='time for clock on the left, defaults to --increment')
	parser.add_argument('-R', '--increment-r', default='', help='time for clock on the right, defaults to --increment')

	parser.add_argument(
		'-f', '--font',
		default='monospace',
		help='the system font to use to display the time',
	)

	args = parser.parse_args()
	return Config(
		time_seconds=parse_time(args.time, incr=False),
		time_l=parse_time(args.time_l, incr=False),
		time_r=parse_time(args.time_r, incr=False),
		increment_seconds=parse_time(args.increment, incr=True),
		increment_l=parse_time(args.increment_l, incr=True),
		increment_r=parse_time(args.increment_r, incr=True),
		font=args.font,
	)
