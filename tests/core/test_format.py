# SPDX-FileCopyrightText: 2024 Boris Stefanovic <owldev@bluewin.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

import random

from chessclock.common import *


def f_time_to_ns(h: int = 0, m: int = 0, s: int = 0, c: int = 0):
	return ((s + 60 * m + 3600 * h) * (10 ** 9)) + (c * (10 ** 7))


def test_time_parts():
	for i in range(100000):
		hmsc = tuple(map(
			lambda x: random.randint(0, x - 1),
			[24, 60, 60, 100],
		))
		ns = f_time_to_ns(*hmsc)
		parts = time_parts(ns)
		assert len(parts) == len(hmsc)
		for expected, actual in zip(hmsc, parts):
			assert expected == actual
