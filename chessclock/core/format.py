from .constants import *
from ..config import Side


def time_parts(ns: int):
	return (
		ns // HOUR,
		(ns // MINUTE) % 60,
		(ns // SECOND) % 60,
		(ns // CENT) % 100,
	)


def time_to_text(ns: int):
	"""
	Converts a duration in nanoseconds to a time representation for humans.
	:param ns: number of nanoseconds
	:return: a "H*:MM:SS.CC" time representation
	"""
	h, m, s, c = time_parts(ns)
	return ''.join((
		f'{h}:' if h != 0 else '',
		f'{m:02d}:' if h != 0 or m != 0 else '',
		f'{s:02d}',
		f'.{c:02d}' if h == 0 and m == 0 else '',
	))


def incr_to_text(ns: int):
	h, m, s, c = time_parts(ns)
	return ''.join((
		f'{h}:' if h else '',
		f'{m:02d}:' if h or m else '',
		f'{s:02d}',
		f'.{c:02d}' if c else '',
	))


def time_control_to_text(t: int, i: int):
	return '+'.join((
		time_to_text(t),
		incr_to_text(i),
	))


def dict_times_to_text(times: dict[Side, int]):
	return {s: time_to_text(t) for s, t in times.items()}
