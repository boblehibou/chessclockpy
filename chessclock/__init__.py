# SPDX-FileCopyrightText: 2024 Boris Stefanovic <owldev@bluewin.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

from chessclock.config import parse_args, Action
from chessclock.core import Core, Side, SECOND
from chessclock.themes import register_local_themes
from chessclock.ui import UI
from .default_interface import DefaultInterface


def main():
	register_local_themes()
	interface = DefaultInterface()
	app = UI(interface)
	app.run()
