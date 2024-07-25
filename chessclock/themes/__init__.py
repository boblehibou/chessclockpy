# SPDX-FileCopyrightText: 2024 Boris Stefanovic <owldev@bluewin.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

import inspect
from typing import Callable

from .theme import Theme

DEFAULT_THEME_NAME = 'default'
THEMES: dict[str, Callable[[], Theme]] = {DEFAULT_THEME_NAME: (lambda: Theme())}


def add_theme(name: str, new_theme: Callable[[], Theme] = Theme, overwrite: bool = False) -> None:
	"""
	Add a theme factory to the known themes.
	:param name: the name of the new theme
	:param new_theme: a callable taking no arguments and returning a subclass of Theme
	:param overwrite: if True, overwrite an existing theme with the same name, if it exists
	:return: None
	"""
	if not isinstance(name, str):
		raise TypeError
	if name in THEMES and not overwrite:
		raise KeyError
	THEMES[name] = new_theme


def get_theme(name: str | None = None, strict: bool = False) -> Theme:
	"""
	Get a theme instance with a given name.
	:param name: the name of the theme
	:param strict: if True, if the given name is not known, raises a KeyError instead of defaulting
	:return: an instance of a theme
	"""
	if name is None:
		name = DEFAULT_THEME_NAME
	if strict and name not in THEMES:
		raise KeyError
	return THEMES.get(name, Theme)()


def list_themes():
	"""
	Get a list of all known theme names.
	:return: a list of all known theme names, in alphabetical order
	"""
	return sorted(THEMES.keys())


def register_local_themes(quiet: bool = False) -> None:
	"""
	Register all themes placed in chessclock/x/themes
	and listed in chessclock/x/themes/__init__.py .
	:return: None
	"""
	from . import extensions as theme_root
	if not quiet:
		print("\n\nAVAILABLE THEMES :\n------------------")
	for name, cl in inspect.getmembers(theme_root, inspect.isclass):
		if issubclass(cl, Theme):
			if not quiet:
				print(cl.get_theme_name())
			add_theme(cl.get_theme_name(), cl)
	if not quiet:
		print()
