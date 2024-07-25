# SPDX-FileCopyrightText: 2024 Boris Stefanovic <owldev@bluewin.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

from .constants import HOUR, MINUTE, SECOND, CENT


def time_parts(ns: int):
	"""
	Split a duration in nanoseconds into common time units.
	Precision is reduced down to a hundredth of a second.
	:param ns: the duration in nanoseconds
	:return: a tuple describing the same duration as (hour, minute, second, hundredth)
	"""
	hmsc = (
		ns // HOUR,
		(ns // MINUTE) % 60,
		(ns // SECOND) % 60,
		(ns // CENT) % 100,
	)
	return hmsc
