#! /usr/bin/python3.11
# -*- coding: utf-8 -*-

# Displays current terminal theme color palette
# Requires: Python 3

# Usage:
# display-colors [OPTIONS]

import click
from collections     import namedtuple
from collections.abc import Generator
from typing          import Callable

SGR_BEG   = '\033['
SGR_END   = 'm'
RESET     = 0
DIM       = 2
MEDIUM    = 22
ITALIC    = 3
BOLD      = 1
REV_VIDEO = 7
UNDERLINE = 4

CODE_COL_WIDTH = 8       ## Widest attr code is '22;97;7m'

FG_COLOR_OFFSET         = 30
BG_COLOR_OFFSET         = 40
DEFAULT_FG_COLOR_OFFSET = 39
DEFAULT_BG_COLOR_OFFSET = 49
BRIGHT_FG_COLOR_OFFSET  = 90
BRIGHT_BG_COLOR_OFFSET  = 100

ALL_WEIGHTS = (
	'Dim',
	'Default',
	'Medium',
	'Bold',
)

WEIGHT_ATTR = {
	'Dim':     DIM,
	'Default': RESET,
	'Medium':  MEDIUM,
	'Bold':    BOLD,
}

WEIGHT_REPR = {
	'Dim':     'Dim',
	'Default': 'Def',
	'Medium':  'Med',
	'Bold':    'Bld',
}

ALL_MISC = {
	'Italic',
	'Reverse-video',
	'Underline',
	'Slow-blink',
	'Rapid-blink',
	'Conceal',
	'Strikethrough',
	'Framed',
	'Encircled',
	'Overlined',
	'Superscript',
	'Subscript',
}

COLORS = (
	'black',
	'red',
	'green',
	'yellow',
	'blue',
	'magenta',
	'cyan',
	'white',
)

COLOR_REPR = {
	'default': 'df',
	'black':   'bk',
	'red':     're',
	'green':   'gr',
	'yellow':  'ye',
	'blue':    'bl',
	'magenta': 'ma',
	'cyan':    'cy',
	'white':   'wh',
}

Switch_Attr = namedtuple('Switch_Attr', ['on', 'off',],)

BG_REPR_ATTR  = dict()
FG_REPR_ATTR  = dict()
EFFECT_SWITCH = dict()

def cat_gens(*gens: list[Generator[str, str, str]]) -> Generator[str, str, str]:
	for gen in gens:
		yield from gen

def color_gen(colors: tuple[str], modifier: Callable) -> Generator[str, str, str]:
	for color in colors:
		yield modifier(COLOR_REPR[color])

def create_attrs(weight: str, fg_repr: str, bg_repr: str, rev_video: bool) -> str:
	(fg, bg) = (bg_repr, fg_repr) if rev_video else (fg_repr, bg_repr)
	return f'{WEIGHT_ATTR[weight]};{FG_REPR_ATTR[fg]};{BG_REPR_ATTR[bg]}' + (f';{REV_VIDEO}' if rev_video else '')

def fg_attr_repr(weight: str, fg_repr: str, rev_video: bool, cell_w: int) -> str:
	rv_attr = f';{REV_VIDEO}' if rev_video else ''
	str     = f'{WEIGHT_ATTR[weight]};{FG_REPR_ATTR[fg_repr]}{rv_attr}m'
	return f'{str:>{cell_w}}'

def colored_cell(attrs: int, text: str) -> str:
	return f'{SGR_BEG}{attrs}{SGR_END}{text}{SGR_BEG}{RESET}{SGR_END}'

def blank_cell(cell_w: int) -> str:
	return colored_cell(create_attrs('Default', 'df', 'df', False), f'{"":{cell_w}}')

def fg_col_gen(weights: list[str], reverse_video: bool, stanzas: bool) -> Generator[str, str, str]:
	col_w = len(COLOR_REPR['default'])
	yield blank_cell(col_w)
	prefix = f''
	for fg_repr in cat_gens(color_gen(('default',), str.lower),
													color_gen(COLORS,       str.lower),
													color_gen(COLORS,       str.upper),
													):
		new_stanza = True
		for _ in weights:
			for _ in (False, True) if reverse_video else (False,):
				attrs = create_attrs('Default', 'df', 'df', False)
				text = f'{prefix}{fg_repr}'
				yield colored_cell(attrs, text) if new_stanza else blank_cell(col_w)
				new_stanza = False
		prefix = f'\n' if stanzas else f''

def weight_col_gen(weights: list[str], reverse_video: bool, header: bool = False) -> Generator[str, str, str]:
	if header:
		yield blank_cell(len(WEIGHT_REPR['Default']))
	for _ in cat_gens(color_gen(('default',), str.lower),
										color_gen(COLORS,       str.lower),
										color_gen(COLORS,       str.upper),
										):
		for weight in weights:
			for rev_video in (False, True) if reverse_video else (False,):
				attrs = create_attrs('Default', 'df', 'df', rev_video)
				text  = f'{WEIGHT_REPR[weight]}'
				yield colored_cell(attrs, text)

def code_col_gen(weights: list[str], reverse_video: bool, col_w: int) -> Generator[str, str, str]:
	yield blank_cell(col_w)
	for fg_repr in cat_gens(color_gen(('default',), str.lower),
													color_gen(COLORS,       str.lower),
													color_gen(COLORS,       str.upper),
													):
		for weight in weights:
			for rev_video in (False, True) if reverse_video else (False,):
				attrs = create_attrs('Default', 'df', 'df', False)
				text  = fg_attr_repr(weight, fg_repr, rev_video, col_w)
				yield colored_cell(attrs, text)

def cell_text(fg_repr: str = '', bg_repr: str = '', text: str = '', transpose: bool = False, cell_w: int = 0) -> str:
	str = f'{fg_repr}/{bg_repr}' if transpose else text
	w   = cell_w or len(str) + 2
	return f'{str:^{w}}'

def column_gen(bg_repr: str, weights: list[str], reverse_video: bool, cell_txt: str, col_w: int, transpose: bool) -> Generator[str, str, str]:
	if not transpose:
		attrs = create_attrs('Default', 'df', 'df', False)
		text  = cell_text(text = f'{BG_REPR_ATTR[bg_repr]}m', cell_w = col_w)
		yield colored_cell(attrs, text)
	for fg_repr in cat_gens(color_gen(('default',), str.lower),
													color_gen(COLORS,       str.lower),
													color_gen(COLORS,       str.upper),
													):
		(fg, bg) = (bg_repr, fg_repr) if transpose else (fg_repr, bg_repr)
		for weight in weights:
			for rev_video in (False, True) if reverse_video else (False,):
				attrs = create_attrs(weight, fg, bg, rev_video)
				text  = cell_text(fg_repr = fg, bg_repr = bg, text = cell_txt, transpose = transpose, cell_w = col_w)
				yield colored_cell(attrs, text)

def display_theme(weights: list[str], reverse_video: bool, cell_txt: str, col_w: int, gutter: str, stanzas: bool, transpose: bool) -> None:
	headers = [
		weight_col_gen(weights, reverse_video),
	] if transpose else [
		fg_col_gen    (weights, reverse_video, stanzas),
		weight_col_gen(weights, reverse_video, header = True),
		code_col_gen  (weights, reverse_video, CODE_COL_WIDTH),
	]
	cols = [column_gen(bg_repr, weights, reverse_video, cell_txt, col_w, transpose)
				 for bg_repr in cat_gens(
					 color_gen(('default',), str.lower),
					 color_gen(COLORS,       str.lower),
					 color_gen(COLORS,       str.upper),
				 )]
	while True:
		try:
			for col in headers:
				print(next(col), end = ' ')
			for col in cols:
				print(next(col), end = gutter)
			print()
		except StopIteration:
			break

def color_text(attrs: str, text: str) -> str:
	return f'{SGR_BEG}{attrs}{SGR_END}{text}'

def test_attributes(neutral_text: str, on_text: str, off_text: str, gutter: str) -> None:
	l_col_w = max(len(name + ':') for name in EFFECT_SWITCH.keys())
	for name, sw in EFFECT_SWITCH.items():
		on_attr  = getattr(sw, 'on')
		off_attr = getattr(sw, 'off')
		label = name + ':'
		print(f'{label:<{l_col_w}}', end = ' ')
		for repr_attr in (FG_REPR_ATTR, BG_REPR_ATTR):
			for modifier in (str.lower, str.upper):
				for color in COLORS:
					color_attr = repr_attr[modifier(COLOR_REPR[color])]
					print(color_text(   color_attr,          neutral_text), end = '')
					print(color_text(f'{color_attr};{on_attr}',   on_text), end = '')
					print(color_text(f'{color_attr};{off_attr}', off_text), end = '')
					print(color_text(RESET, ''), end = gutter)
		print()

def init_display_attributes(d: dict[str, str]) -> None:
	def init_attribute(name: str, on: str, off: str) -> None:
		d[name] = Switch_Attr(on = on, off = off)

	for name, on, off in (
		('Italic',       '3', '23'),
		('Dim',          '2', '22'),
		('Medium',      '22', '22'),
		('Bold',         '1', '21'),
		('Rev video',    '7', '27'),
		('Underline',    '4', '24'),
		('2xUnderline', '21', '24'),
		('Slow blink',   '5', '25'),
		('Rapid blink',  '6', '25'),
		('Conceal',      '8', '28'),
		('Strikethru',   '9', '29'),
		('Framed',      '51', '54'),
		('Encircled',   '52', '54'),
		('Overlined',   '53', '55'),
		('Fraktur',     '20', '23'),
		('Superscript', '73', '75'),
		('Subscript',   '74', '75'),
		):
		init_attribute(name, on, off)

def init_mappings() -> None:
	def init_mapping(target: dict[str, str], colors: tuple[str], offset: int, modifier: Callable) -> None:
		for code, color in enumerate(colors, start = offset):
			target[modifier(COLOR_REPR[color])] = code

	for target, colors, offset, modifier in (
		(FG_REPR_ATTR, COLORS,               FG_COLOR_OFFSET, str.lower),
		(FG_REPR_ATTR, ('default',), DEFAULT_FG_COLOR_OFFSET, str.lower),
		(FG_REPR_ATTR, COLORS,        BRIGHT_FG_COLOR_OFFSET, str.upper),
		(BG_REPR_ATTR, COLORS,               BG_COLOR_OFFSET, str.lower),
		(BG_REPR_ATTR, ('default',), DEFAULT_BG_COLOR_OFFSET, str.lower),
		(BG_REPR_ATTR, COLORS,        BRIGHT_BG_COLOR_OFFSET, str.upper),
	):
		init_mapping(target, colors, offset, modifier)

@click.command()
@click.option('--col-width',     '_col_w',        type = int,  help = "Column width",                                                  default = 7,     show_default = True)
@click.option('--gutter',        '_gutter',       type = str,  help = "String delimiting output columns  [default: empty string]",     default = '',    show_default = True)
@click.option('--pattern',       '_pattern',      type = str,  help = "Sample pattern character for the --test option",                default = '|',   show_default = True)
@click.option('--reverse-video', '_rev_video', is_flag = True, help = "Add 'background-color on foreground-color' in reverse video",   default = False, show_default = True)
@click.option('--stanzas',       '_stanzas',   is_flag = True, help = "Group output rows by color (non-transposed only)",              default = False, show_default = True)
@click.option('--test',          '_test',      is_flag = True, help = "Display samples of SGR terminal effects in the normal and bright colors", default = False, show_default = True)
@click.option('--text',          '_text',         type = str,  help = "Sample text in each cell (non-transposed only)",                default = 'gYw', show_default = True)
@click.option('--transpose',     '_transpose', is_flag = True, help = "Display foreground colors in column-major order  [default: row-major order]", default = False, show_default = True)
@click.version_option(package_name = 'display-colors')
@click.option('--weight', '-w',  '_weights',      type = click.Choice(['dim', 'default', 'medium', 'bold', 'all'], case_sensitive = False), multiple = True, help = "Which weight font to display (use multiple times)", default = ['default', 'bold'], show_default = True)
def main(_transpose: bool, _weights: list[str], _rev_video: bool, _col_w: int, _gutter: str, _stanzas: bool, _text: str, _test: bool, _pattern: str) -> None:
	init_mappings()
	if _test:
		init_display_attributes(EFFECT_SWITCH)
		test_attributes(_pattern, _pattern, _pattern, _gutter)
		exit()
	weights = ALL_WEIGHTS if 'all' in _weights else [w.capitalize() for w in _weights]
	display_theme(weights, _rev_video, _text, col_w = _col_w, gutter = _gutter, stanzas = _stanzas, transpose = _transpose)

if __name__ == '__main__':
	main()
