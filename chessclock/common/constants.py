# SPDX-FileCopyrightText: 2024 Boris Stefanovic <owldev@bluewin.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

"""
A few constants representing the values of common time units in nanoseconds.
Designed to work with time.time_ns().
"""

CENT: int = 10 ** 7
SECOND: int = 100 * CENT
MINUTE: int = 60 * SECOND
HOUR: int = 60 * MINUTE
DAY: int = 24 * HOUR
