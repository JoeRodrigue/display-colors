#! /usr/bin/python3.11
# -*- coding: utf-8 -*-

# Displays current terminal theme color palette
# Requires: Python 3

# Usage:
# display-colors [OPTIONS]

# Copyright (C) 2024 Joe Rodrigue <joe.rodrigue at gmail dot com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click

from display_colors.cmd.effects   import display_effects
from display_colors.cmd.four_bit  import display_4_bit
from display_colors.cmd.eight_bit import display_8_bit
from display_colors.init          import init_mappings

@click.group()
@click.version_option(package_name = 'display-colors')
def cli():
	"""Prints test patterns to show the color and display effect capabilities of a terminal emulator"""
	init_mappings()

cli.add_command(display_4_bit)
cli.add_command(display_8_bit)
cli.add_command(display_effects)

if __name__ == '__main__':
	cli()

# SGR_BEG   = '\033['
# SGR_END   = 'm'
# RESET     = 0
# DIM       = 2
# MEDIUM    = 22
# ITALIC    = 3
# BOLD      = 1
# REV_VIDEO = 7
# UNDERLINE = 4

# _8_BIT_FG_PREFIX = '38;5;'
# _8_BIT_BG_PREFIX = '48;5;'

# CODE_COL_WIDTH = 8       ## Widest attr code is '22;97;7m'

# _4_BIT_FG_COLOR_OFFSET         = 30
# _4_BIT_BG_COLOR_OFFSET         = 40
# _4_BIT_DEFAULT_FG_COLOR_OFFSET = 39
# _4_BIT_DEFAULT_BG_COLOR_OFFSET = 49
# _4_BIT_BRIGHT_FG_COLOR_OFFSET  = 90
# _4_BIT_BRIGHT_BG_COLOR_OFFSET  = 100
# _8_BIT_FG_COLOR_OFFSET         = 0
# _8_BIT_BG_COLOR_OFFSET         = 0
# _8_BIT_BRIGHT_FG_COLOR_OFFSET  = 8
# _8_BIT_BRIGHT_BG_COLOR_OFFSET  = 8

# _4_BIT_FG_STANDARD_OFFSET = 30
# _4_BIT_FG_BRIGHT_OFFSET   = 90
# _4_BIT_FG_DEFAULT_OFFSET  = 39
# _4_BIT_BG_STANDARD_OFFSET = 40
# _4_BIT_BG_BRIGHT_OFFSET   = 100
# _4_BIT_BG_DEFAULT_OFFSET  = 49

# _8_BIT_STANDARD_OFFSET  = 0
# _8_BIT_BRIGHT_OFFSET    = 8
# _8_BIT_PALETTE_OFFSET   = 16
# # _8_BIT_GRAYSCALE_OFFSET = 232

# _8_BIT_COLORS_N         = 256
# _8_BIT_PALETTE_N        = _8_BIT_GRAYSCALE_OFFSET - _8_BIT_PALETTE_OFFSET
# _8_BIT_GRAYSCALE_N      = _8_BIT_COLORS_N         - _8_BIT_GRAYSCALE_OFFSET

# _8_BIT_PALETTE_CUBE_SIDE = 6

# ALL_WEIGHTS = (
# 	'Dim',
# 	'Default',
# 	'Medium',
# 	'Bold',
# )

# WEIGHT_ATTR = {
# 	'Dim':     DIM,
# 	'Default': RESET,
# 	'Medium':  MEDIUM,
# 	'Bold':    BOLD,
# }

# WEIGHT_REPR = {
# 	'Dim':     'Dim',
# 	'Default': 'Def',
# 	'Medium':  'Med',
# 	'Bold':    'Bld',
# }

# ALL_MISC = {
# 	'Italic',
# 	'Reverse-video',
# 	'Underline',
# 	'Slow-blink',
# 	'Rapid-blink',
# 	'Conceal',
# 	'Strikethrough',
# 	'Framed',
# 	'Encircled',
# 	'Overlined',
# 	'Superscript',
# 	'Subscript',
# }

# COLORS = (
# 	'black',
# 	'red',
# 	'green',
# 	'yellow',
# 	'blue',
# 	'magenta',
# 	'cyan',
# 	'white',
# )

# COLOR_REPR = {
# 	'default': 'df',
# 	'black':   'bk',
# 	'red':     're',
# 	'green':   'gr',
# 	'yellow':  'ye',
# 	'blue':    'bl',
# 	'magenta': 'ma',
# 	'cyan':    'cy',
# 	'white':   'wh',
# }

# Switch_Attr = namedtuple('Switch_Attr', ['on', 'off',],)

# _4_BIT_BG_REPR_ATTR  = dict()
# _4_BIT_FG_REPR_ATTR  = dict()
# _8_BIT_BG_REPR_ATTR  = dict()
# _8_BIT_FG_REPR_ATTR  = dict()
# EFFECT_SWITCH       = dict()

# def cat_gens(*gens: list[Generator[str, str, str]]) -> Generator[str, str, str]:
# 	for gen in gens:
# 		yield from gen

# def color_gen(colors: tuple[str], modifier: Callable) -> Generator[str, str, str]:
# 	for color in colors:
# 		yield modifier(COLOR_REPR[color])

# def create_attrs(weight: str, fg_repr: str, bg_repr: str, rev_video: bool = False, _8_bit: bool = False) -> str:
# 	(fg, bg) = (bg_repr, fg_repr) if rev_video else (fg_repr, bg_repr)
# 	(fg_repr_attr, bg_repr_attr) = (_8_BIT_FG_REPR_ATTR, _8_BIT_BG_REPR_ATTR) if _8_bit else (_4_BIT_FG_REPR_ATTR, _4_BIT_BG_REPR_ATTR)
# 	rev_video_attr = f';{REV_VIDEO}' if rev_video else f''
# 	return f'{WEIGHT_ATTR[weight]};{fg_repr_attr[fg]};{bg_repr_attr[bg]}{rev_video_attr}'

# def fg_attr_repr(weight: str, fg_repr: str, rev_video: bool, cell_w: int) -> str:
# 	rv_attr = f';{REV_VIDEO}' if rev_video else ''
# 	str     = f'{WEIGHT_ATTR[weight]};{_4_BIT_FG_REPR_ATTR[fg_repr]}{rv_attr}m'
# 	return f'{str:>{cell_w}}'

# def colored_cell(attrs: int, text: str) -> str:
# 	return f'{SGR_BEG}{attrs}{SGR_END}{text}{SGR_BEG}{RESET}{SGR_END}'

# def blank_cell(cell_w: int) -> str:
# 	return colored_cell(create_attrs('Default', 'df', 'df'), f'{"":{cell_w}}')

# def fg_col_gen(weights: list[str], reverse_video: bool, stanzas: bool) -> Generator[str, str, str]:
# 	col_w = len(COLOR_REPR['default'])
# 	yield blank_cell(col_w)
# 	prefix = f''
# 	for fg_repr in cat_gens(color_gen(('default',), str.lower),
# 													color_gen(COLORS,       str.lower),
# 													color_gen(COLORS,       str.upper),
# 													):
# 		new_stanza = True
# 		for _ in weights:
# 			for _ in (False, True) if reverse_video else (False,):
# 				attrs = create_attrs('Default', 'df', 'df')
# 				text = f'{prefix}{fg_repr}'
# 				yield colored_cell(attrs, text) if new_stanza else blank_cell(col_w)
# 				new_stanza = False
# 		prefix = f'\n' if stanzas else f''

# def weight_col_gen(weights: list[str], reverse_video: bool, header: bool = False) -> Generator[str, str, str]:
# 	if header:
# 		yield blank_cell(len(WEIGHT_REPR['Default']))
# 	for _ in cat_gens(color_gen(('default',), str.lower),
# 										color_gen(COLORS,       str.lower),
# 										color_gen(COLORS,       str.upper),
# 										):
# 		for weight in weights:
# 			for rev_video in (False, True) if reverse_video else (False,):
# 				attrs = create_attrs('Default', 'df', 'df', rev_video = rev_video)
# 				text  = f'{WEIGHT_REPR[weight]}'
# 				yield colored_cell(attrs, text)

# def code_col_gen(weights: list[str], reverse_video: bool, col_w: int) -> Generator[str, str, str]:
# 	yield blank_cell(col_w)
# 	for fg_repr in cat_gens(color_gen(('default',), str.lower),
# 													color_gen(COLORS,       str.lower),
# 													color_gen(COLORS,       str.upper),
# 													):
# 		for weight in weights:
# 			for rev_video in (False, True) if reverse_video else (False,):
# 				attrs = create_attrs('Default', 'df', 'df')
# 				text  = fg_attr_repr(weight, fg_repr, rev_video, col_w)
# 				yield colored_cell(attrs, text)

# def cell_text(fg_repr: str = '', bg_repr: str = '', text: str = '', transpose: bool = False, cell_w: int = 0) -> str:
# 	str = f'{fg_repr}/{bg_repr}' if transpose else text
# 	w   = cell_w or len(str) + 2
# 	return f'{str:^{w}}'

# def column_gen(bg_repr: str, weights: list[str], reverse_video: bool, cell_txt: str, col_w: int, transpose: bool) -> Generator[str, str, str]:
# 	if not transpose:
# 		attrs = create_attrs('Default', 'df', 'df')
# 		text  = cell_text(text = f'{_4_BIT_BG_REPR_ATTR[bg_repr]}m', cell_w = col_w)
# 		yield colored_cell(attrs, text)
# 	for fg_repr in cat_gens(color_gen(('default',), str.lower),
# 													color_gen(COLORS,       str.lower),
# 													color_gen(COLORS,       str.upper),
# 													):
# 		(fg, bg) = (bg_repr, fg_repr) if transpose else (fg_repr, bg_repr)
# 		for weight in weights:
# 			for rev_video in (False, True) if reverse_video else (False,):
# 				attrs = create_attrs(weight, fg, bg, rev_video = rev_video)
# 				text  = cell_text(fg_repr = fg, bg_repr = bg, text = cell_txt, transpose = transpose, cell_w = col_w)
# 				yield colored_cell(attrs, text)

# def eight_bit_hdrs_gen() -> Generator[str, str, str]:
# 	for s in ('8-bit', '4-bit'):
# 		yield s

# def eight_bit_col_gen(bg_repr: str, code: int, col_w: int) -> Generator[str, str, str]:
# 	(fg_color, fg_modifier) = ('white', str.upper) if bg_repr.islower() else ('black', str.lower)
# 	fg_repr = fg_modifier(COLOR_REPR[fg_color])
# 	for _8_bit in (True, False):
# 		attrs = create_attrs('Default', fg_repr, bg_repr, _8_bit = _8_bit)
# 		text  = cell_text(text = f'{code:X}', cell_w = col_w)
# 		yield colored_cell(attrs, text)

# # def rev_base_n_to_decimal(n: int, *digits: list[int]) -> int:
# # 	def cont(result: int, digit_list: list[int]) -> int:
# # 		return result if not digit_list else cont((result * n) + digit_list[-1], digit_list[:-1])

# # 	return cont(0, digits)

# def eight_bit_palette(col_w: int, orientation: str) -> None:
# 	match (orientation):
# 		case 'xyz': posn_delta = lambda x, y, z: rev_base_n_to_decimal(_8_BIT_PALETTE_CUBE_SIDE, x, y, z)
# 		case 'xzy': posn_delta = lambda x, y, z: rev_base_n_to_decimal(_8_BIT_PALETTE_CUBE_SIDE, x, z, y)
# 		case 'zyx': posn_delta = lambda x, y, z: rev_base_n_to_decimal(_8_BIT_PALETTE_CUBE_SIDE, z, y, x)
# 		case _: raise Exception(f'eight_bit_palette: unknown orientation {orientation}')
# 	for y in range(_8_BIT_PALETTE_CUBE_SIDE):
# 		for z in range(_8_BIT_PALETTE_CUBE_SIDE):
# 			for x in range(_8_BIT_PALETTE_CUBE_SIDE):
# 				delta = posn_delta(x, y, z)
# 				code  = delta + _8_BIT_PALETTE_OFFSET
# 				fg_repr = "bk" if (delta // (_8_BIT_PALETTE_CUBE_SIDE * _8_BIT_PALETTE_CUBE_SIDE / 2)) % 2 else "WH"
# 				attrs = f'{_8_BIT_FG_REPR_ATTR[fg_repr]};{_8_BIT_BG_REPR_ATTR[str(code)]}'
# 				text  = cell_text(text = f'{code:X}', cell_w = col_w)
# 				print(colored_cell(attrs, text), end = '')
# 			print(' ', end = '')
# 		print()

# def eight_bit_grayscale(col_w: int) -> None:
# 	halfway = _8_BIT_GRAYSCALE_OFFSET + (_8_BIT_GRAYSCALE_N / 2)
# 	for code in range(_8_BIT_GRAYSCALE_OFFSET, _8_BIT_COLORS_N):
# 		fg_repr = COLOR_REPR['white'].upper() if code < halfway else COLOR_REPR['black'].lower()
# 		attrs = create_attrs('Default', fg_repr, str(code), _8_bit = True)
# 		text  = cell_text(text = f'{code:X}', cell_w = col_w)
# 		print(colored_cell(attrs, text), end = '')
# 	print()

# def eight_bit(col_w: int) -> None:
# 	headers = [eight_bit_hdrs_gen()]
# 	cols = [eight_bit_col_gen(bg_repr, code, col_w)
# 				 for code, bg_repr in enumerate(cat_gens(
# 					 color_gen(COLORS,       str.lower),
# 					 color_gen(COLORS,       str.upper),
# 				 ))]
# 	print('Standard and bright colors:')
# 	while True:
# 		try:
# 			for col in headers:
# 				print(next(col), end = ' ')
# 			for col in cols:
# 				print(next(col), end = '')
# 			print()
# 		except StopIteration:
# 			break
# 	print('RGB palette cube, front:')
# 	eight_bit_palette(3, 'xyz')
# 	print('Top:')
# 	eight_bit_palette(3, 'xzy')
# 	print('Left side:')
# 	eight_bit_palette(3, 'zyx')
# 	print('Grayscale:')
# 	eight_bit_grayscale(5)

# def display_theme(weights: list[str], reverse_video: bool, cell_txt: str, col_w: int, gutter: str, stanzas: bool, transpose: bool) -> None:
# 	headers = [
# 		weight_col_gen(weights, reverse_video),
# 	] if transpose else [
# 		fg_col_gen    (weights, reverse_video, stanzas),
# 		weight_col_gen(weights, reverse_video, header = True),
# 		code_col_gen  (weights, reverse_video, CODE_COL_WIDTH),
# 	]
# 	cols = [column_gen(bg_repr, weights, reverse_video, cell_txt, col_w, transpose)
# 				 for bg_repr in cat_gens(
# 					 color_gen(('default',), str.lower),
# 					 color_gen(COLORS,       str.lower),
# 					 color_gen(COLORS,       str.upper),
# 				 )]
# 	while True:
# 		try:
# 			for col in headers:
# 				print(next(col), end = ' ')
# 			for col in cols:
# 				print(next(col), end = gutter)
# 			print()
# 		except StopIteration:
# 			break

# def color_text(attrs: str, text: str) -> str:
# 	return f'{SGR_BEG}{attrs}{SGR_END}{text}'

# def test_attributes(neutral_text: str, on_text: str, off_text: str, gutter: str) -> None:
# 	l_col_w = max(len(name + ':') for name in EFFECT_SWITCH.keys())
# 	for name, sw in EFFECT_SWITCH.items():
# 		on_attr  = getattr(sw, 'on')
# 		off_attr = getattr(sw, 'off')
# 		label = name + ':'
# 		print(f'{label:<{l_col_w}}', end = ' ')
# 		for repr_attr in (_4_BIT_FG_REPR_ATTR, _4_BIT_BG_REPR_ATTR):
# 			for modifier in (str.lower, str.upper):
# 				for color in COLORS:
# 					color_attr = repr_attr[modifier(COLOR_REPR[color])]
# 					print(color_text(   color_attr,          neutral_text), end = '')
# 					print(color_text(f'{color_attr};{on_attr}',   on_text), end = '')
# 					print(color_text(f'{color_attr};{off_attr}', off_text), end = '')
# 					print(color_text(RESET, ''), end = gutter)
# 		print()

# def init_display_attributes(d: dict[str, str]) -> None:
# 	def init_attribute(name: str, on: str, off: str) -> None:
# 		d[name] = Switch_Attr(on = on, off = off)

# 	for name, on, off in (
# 		('Italic',       '3', '23'),
# 		('Dim',          '2', '22'),
# 		('Medium',      '22', '22'),
# 		('Bold',         '1', '21'),
# 		('Rev video',    '7', '27'),
# 		('Underline',    '4', '24'),
# 		('2xUnderline', '21', '24'),
# 		('Slow blink',   '5', '25'),
# 		('Rapid blink',  '6', '25'),
# 		('Conceal',      '8', '28'),
# 		('Strikethru',   '9', '29'),
# 		('Framed',      '51', '54'),
# 		('Encircled',   '52', '54'),
# 		('Overlined',   '53', '55'),
# 		('Fraktur',     '20', '23'),
# 		('Superscript', '73', '75'),
# 		('Subscript',   '74', '75'),
# 		):
# 		init_attribute(name, on, off)

# def init_mappings() -> None:
# 	def init_mapping(target: dict[str, str], colors: tuple[str], offset: int, modifier: Callable, prefix: str) -> None:
# 		for code, color in enumerate(colors, start = offset):
# 			target[modifier(COLOR_REPR[color])] = f'{prefix}{code}'

# 	def init_palette(target: dict[str, str], n: int, offset: int, prefix: str) -> None:
# 		for code in range(offset, offset + n):
# 			target[str(code)] = f'{prefix}{code}'

# 	for target, colors, offset, modifier, prefix in (
# 		(_4_BIT_FG_REPR_ATTR, COLORS,               _4_BIT_FG_COLOR_OFFSET, str.lower, ''),
# 		(_4_BIT_FG_REPR_ATTR, ('default',), _4_BIT_DEFAULT_FG_COLOR_OFFSET, str.lower, ''),
# 		(_4_BIT_FG_REPR_ATTR, COLORS,        _4_BIT_BRIGHT_FG_COLOR_OFFSET, str.upper, ''),
# 		(_4_BIT_BG_REPR_ATTR, COLORS,               _4_BIT_BG_COLOR_OFFSET, str.lower, ''),
# 		(_4_BIT_BG_REPR_ATTR, ('default',), _4_BIT_DEFAULT_BG_COLOR_OFFSET, str.lower, ''),
# 		(_4_BIT_BG_REPR_ATTR, COLORS,        _4_BIT_BRIGHT_BG_COLOR_OFFSET, str.upper, ''),

# 		(_8_BIT_FG_REPR_ATTR, COLORS,               _8_BIT_FG_COLOR_OFFSET, str.lower, _8_BIT_FG_PREFIX),
# 		(_8_BIT_FG_REPR_ATTR, COLORS,        _8_BIT_BRIGHT_FG_COLOR_OFFSET, str.upper, _8_BIT_FG_PREFIX),
# 		(_8_BIT_BG_REPR_ATTR, COLORS,               _8_BIT_BG_COLOR_OFFSET, str.lower, _8_BIT_BG_PREFIX),
# 		(_8_BIT_BG_REPR_ATTR, COLORS,        _8_BIT_BRIGHT_BG_COLOR_OFFSET, str.upper, _8_BIT_BG_PREFIX),
# 	):
# 		init_mapping(target, colors, offset, modifier, prefix)

# 	for target, n, offset, prefix in (
# 		(_8_BIT_FG_REPR_ATTR, _8_BIT_COLORS_N - _8_BIT_PALETTE_OFFSET, _8_BIT_PALETTE_OFFSET, _8_BIT_FG_PREFIX),
# 		(_8_BIT_BG_REPR_ATTR, _8_BIT_COLORS_N - _8_BIT_PALETTE_OFFSET, _8_BIT_PALETTE_OFFSET, _8_BIT_BG_PREFIX),
# 	):
# 		init_palette(target, n, offset, prefix)

# @click.command()
# @click.option('--8-bit',         '_8_bit',     is_flag = True, help = "Display 8-bit colors",                                          default = False, show_default = True)
# @click.option('--col-width',     '_col_w',        type = int,  help = "Column width",                                                  default = 7,     show_default = True)
# @click.option('--gutter',        '_gutter',       type = str,  help = "String delimiting output columns  [default: empty string]",     default = '',    show_default = True)
# @click.option('--pattern',       '_pattern',      type = str,  help = "Sample pattern character for the --test option",                default = '|',   show_default = True)
# @click.option('--reverse-video', '_rev_video', is_flag = True, help = "Add 'background-color on foreground-color' in reverse video",   default = False, show_default = True)
# @click.option('--stanzas',       '_stanzas',   is_flag = True, help = "Group output rows by color (non-transposed only)",              default = False, show_default = True)
# @click.option('--test',          '_test',      is_flag = True, help = "Display samples of SGR terminal effects in the normal and bright colors", default = False, show_default = True)
# @click.option('--text',          '_text',         type = str,  help = "Sample text in each cell (non-transposed only)",                default = 'gYw', show_default = True)
# @click.option('--transpose',     '_transpose', is_flag = True, help = "Display foreground colors in column-major order  [default: row-major order]", default = False, show_default = True)
# @click.version_option(package_name = 'display-colors')
# @click.option('--weight', '-w',  '_weights',      type = click.Choice(['dim', 'default', 'medium', 'bold', 'all'], case_sensitive = False), multiple = True, help = "Which weight font to display (use multiple times)", default = ['default', 'bold'], show_default = True)
# def main(_transpose: bool, _8_bit: bool, _weights: list[str], _rev_video: bool, _col_w: int, _gutter: str, _stanzas: bool, _text: str, _test: bool, _pattern: str) -> None:
# 	init_mappings()
# 	if _test:
# 		# init_display_attributes(EFFECT_SWITCH)
# 		# test_attributes(_pattern, _pattern, _pattern, _gutter)
# 		exit()
# 	elif _8_bit:
# 		pass
# 		# eight_bit(col_w = _col_w)
# 	else:
# 		pass
# 		# weights = ALL_WEIGHTS if 'all' in _weights else [w.capitalize() for w in _weights]
# 		# display_theme(weights, _rev_video, _text, col_w = _col_w, gutter = _gutter, stanzas = _stanzas, transpose = _transpose)

# from collections.abc import Generator
# from typing          import Callable

