#! /usr/bin/python3.11
# -*- coding: utf-8 -*-

# Displays current terminal theme color palette
# Requires: Python 3.10+

# Usage:
# display-colors [OPTIONS]

import click
from collections.abc import Generator
from typing          import Callable

ANSI_BEG  = '\033['
ANSI_END  = 'm'
BOLD      = 1
DIM       = 2
MEDIUM    = 22
RESET     = 0
REV_VIDEO = 7
UNDERLINE = 4

FG_COLOR_OFFSET         = 30
BG_COLOR_OFFSET         = 40
DEFAULT_FG_COLOR_OFFSET = 39
DEFAULT_BG_COLOR_OFFSET = 49
BRIGHT_FG_COLOR_OFFSET  = 90
BRIGHT_BG_COLOR_OFFSET  = 100

ALL_INTENSITIES = (
	'Dim',
	'Default',
	'Medium',
	'Bold',
)

STANDARD_INTENSITIES = (
	'Default',
	'Bold',
)

INTENSITY_ATTR = {
	'Dim':     DIM,
	'Default': RESET,
	'Medium':  MEDIUM,
	'Bold':    BOLD,
}

INTENSITY_REPR = {
	'Dim':     'Dim',
	'Default': 'Def',
	'Medium':  'Med',
	'Bold':    'Bld',
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

BG_REPR_ATTR = dict()
FG_REPR_ATTR = dict()

def color_gen(colors: tuple[str], modifier: Callable) -> Generator[str, str, str]:
	for color in colors:
		yield modifier(COLOR_REPR[color])

def cat_gens(*gens: list[Generator[int, int, int]]) -> Generator[int, int, int]:
	for gen in gens:
		yield from gen

def print_all_combinations(intensities: list[str], l_col_w: int, cell_w: int, reverse_video: bool, gutter: str) -> None:
	display_top_headers(l_col_w, cell_w, gutter)

def print_all_combinations_old(intensity_attr: int, reverse_video: bool, gutter: str) -> None:
	for bg_repr in cat_gens(color_gen(('default',), str.lower),
														  color_gen(COLORS,       str.lower),
															color_gen(COLORS,       str.upper),
														 ):
		for rev_video in (False, True) if reverse_video else (False,):
			display_left_header()
			for fg_repr in cat_gens(color_gen(('default',), str.lower),
																	color_gen(COLORS,       str.lower),
																	color_gen(COLORS,       str.upper),
																):
				print_cell(fg_repr, bg_repr, intensity_attr, rev_video, gutter)
			print()

def print_cell(fg_repr: str, bg_repr: str, intensity_attr: int, rev_video: bool, gutter: str) -> None:
	(fg, bg) = (bg_repr, fg_repr) if rev_video else (fg_repr, bg_repr)
	attrs    = f'{intensity_attr};{FG_REPR_ATTR[fg]};{BG_REPR_ATTR[bg]}' + (f';{REV_VIDEO}' if rev_video else '')
	str      = f'{fg_repr}/{bg_repr}'
	cell_w   = len(str) + 2
	print(f'{ANSI_BEG}{attrs}{ANSI_END}{str:^{cell_w}}{ANSI_BEG}{RESET}{ANSI_END}', end = gutter)

def create_attrs(intensity: str, fg_repr: str, bg_repr: str, rev_video: bool) -> str:
	(fg, bg) = (bg_repr, fg_repr) if rev_video else (fg_repr, bg_repr)
	return f'{INTENSITY_ATTR[intensity]};{FG_REPR_ATTR[fg]};{BG_REPR_ATTR[bg]}' + (f';{REV_VIDEO}' if rev_video else '')

def display_top_headers(l_col_w: int, cell_w: int, gutter: str) -> None:
	attrs = create_attrs('Default', 'df', 'df', False)
	text  = cell_text(text = '', cell_w = l_col_w)
	display_cell(attrs, text, ' ')
	for bg_repr in cat_gens(color_gen(('default',), str.lower),
															color_gen(COLORS,       str.lower),
															color_gen(COLORS,       str.upper),
															):
		txt  = f'{BG_REPR_ATTR[bg_repr]}m'
		text = cell_text(text = txt, cell_w = cell_w)
		display_cell(attrs, text, gutter)
	print()

def fg_attr_repr(intensity: str, fg_repr: str, rev_video: bool, cell_w: int) -> str:
	rv_attr = f';{REV_VIDEO}' if rev_video else ''
	str     = f'{INTENSITY_ATTR[intensity]};{FG_REPR_ATTR[fg_repr]}{rv_attr}m'
	return f'{str:>{cell_w}}'

def display_left_header(intensity: str, ground_attr: int, rev_video: bool, l_col_w: int) -> None:
	attrs = create_attrs('Default', 'df', 'df', rev_video)
	text  = f'{INTENSITY_REPR[intensity]}'
	display_cell(attrs, text, ' ')
	attrs = create_attrs('Default', 'df', 'df', False)
	text  = fg_attr_repr(intensity, ground_attr, rev_video, l_col_w)
	display_cell(attrs, text, ' ')

def colored_cell(attrs: int, text: str) -> str:
	return f'{ANSI_BEG}{attrs}{ANSI_END}{text}{ANSI_BEG}{RESET}{ANSI_END}'

def blank_cell(cell_w: int) -> str:
	return colored_cell(create_attrs('Default', 'df', 'df', False), f'{"":{cell_w}}')

def intensity_col_gen(intensities: list[str], reverse_video: bool) -> Generator[str, str, str]:
	yield blank_cell(len(INTENSITY_REPR['Default']))
	for _ in cat_gens(color_gen(('default',), str.lower),
										color_gen(COLORS,       str.lower),
										color_gen(COLORS,       str.upper),
										):
		for intensity in intensities:
			for rev_video in (False, True) if reverse_video else (False,):
				attrs = create_attrs('Default', 'df', 'df', rev_video)
				text  = f'{INTENSITY_REPR[intensity]}'
				yield colored_cell(attrs, text)

def code_col_gen(intensities: list[str], reverse_video: bool, cell_w: int) -> Generator[str, str, str]:
	yield blank_cell(cell_w)
	for fg_repr in cat_gens(color_gen(('default',), str.lower),
													color_gen(COLORS,       str.lower),
													color_gen(COLORS,       str.upper),
													):
		for intensity in intensities:
			for rev_video in (False, True) if reverse_video else (False,):
				attrs = create_attrs('Default', 'df', 'df', False)
				text  = fg_attr_repr(intensity, fg_repr, rev_video, cell_w)
				yield colored_cell(attrs, text)

def fg_col_gen(intensities: list[str], reverse_video: bool) -> Generator[str, str, str]:
	col_w = len(COLOR_REPR['default'])
	yield blank_cell(col_w)
	prefix = f''
	for fg_repr in cat_gens(color_gen(('default',), str.lower),
													color_gen(COLORS,       str.lower),
													color_gen(COLORS,       str.upper),
													):
		new_stanza = True
		for _ in intensities:
			for _ in (False, True) if reverse_video else (False,):
				attrs = create_attrs('Default', 'df', 'df', False)
				text = f'{prefix}{fg_repr}'
				yield colored_cell(attrs, text) if new_stanza else blank_cell(col_w)
				new_stanza = False
		prefix = f'\n'

def display_theme(intensities: list[str], reverse_video: bool, code_col_w: int, cell_txt: str, cell_w: int, gutter: str) -> None:
	headers = [
		fg_col_gen       (intensities, reverse_video),
		intensity_col_gen(intensities, reverse_video),
		code_col_gen     (intensities, reverse_video, code_col_w),
	]
	cols = [column_gen(bg_repr, intensities, reverse_video, cell_txt, cell_w)
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

def column_gen(bg_repr: str, intensities: list[str], reverse_video: bool, cell_txt: str, col_w: int) -> Generator[str, str, str]:
	attrs = create_attrs('Default', 'df', 'df', False)
	text  = cell_text(text = f'{BG_REPR_ATTR[bg_repr]}m', cell_w = col_w)
	yield colored_cell(attrs, text)
	for fg_repr in cat_gens(color_gen(('default',), str.lower),
													color_gen(COLORS,       str.lower),
													color_gen(COLORS,       str.upper),
													):
		for intensity in intensities:
			for rev_video in (False, True) if reverse_video else (False,):
				attrs = create_attrs(intensity, fg_repr, bg_repr, rev_video)
				text  = cell_text(text = cell_txt, cell_w = col_w)
				yield colored_cell(attrs, text)

def display_theme_old(intensities: list[str], reverse_video: bool, l_col_w: int, cell_txt: str, cell_w: int, gutter: str) -> None:
	display_top_headers(l_col_w + 4, cell_w, gutter)
	for fg_repr in cat_gens(color_gen(('default',), str.lower),
														  color_gen(COLORS,       str.lower),
															color_gen(COLORS,       str.upper),
														 ):
		for intensity in intensities:
			for rev_video in (False, True) if reverse_video else (False,):
				display_left_header(intensity, FG_REPR_ATTR[fg_repr], rev_video, l_col_w)
				for bg_repr in cat_gens(color_gen(('default',), str.lower),
																		color_gen(COLORS,       str.lower),
																		color_gen(COLORS,       str.upper),
																	):
					attrs = create_attrs(intensity, fg_repr, bg_repr, rev_video)
					text = cell_text(text = cell_txt, cell_w = cell_w)
					display_cell(attrs, text, gutter)
				print()
		print()

def cell_text_theme(fg_repr: str, bg_repr: str) -> str:
	return cell_text(f'{fg_repr}/{bg_repr}')

def cell_text(fg_repr: str = '', bg_repr: str = '', text: str = '', cell_w: int = 0) -> str:
	str = f'{fg_repr}/{bg_repr}' if fg_repr else text
	w   = cell_w or len(str) + 2
	return f'{str:^{cell_w}}'

def display_cell(attrs: str, text: str, gutter: str) -> None:
	print(f'{ANSI_BEG}{attrs}{ANSI_END}{text}{ANSI_BEG}{RESET}{ANSI_END}', end = gutter)

def init_mappings() -> None:
	def init_mapping(target: dict[str, int], colors: tuple[str], offset: int, modifier: Callable) -> None:
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
@click.option('--standard',                         '_standard',   is_flag = True,  help = "Print the standard theme format", default = False, show_default = True)
@click.option('--complete',                         '_complete',   is_flag = True,  help = "Print the complete theme format", default = False, show_default = True)
@click.option('--intensities',                      '_intensities',   type = click.Choice(['standard', 'all'], case_sensitive = False),  help = "(default, bold) or (dim, default, medium, bold)", default = 'standard', show_default = True)
@click.option('--reverse-video/--no-reverse-video', '_reverse_video', type = bool, help = "Add 'background-color on foreground-color' in reverse video",   default = False,      show_default = True)
@click.option('--standard-cell-width',              '_scell_w',       type = int,  help = "Cell width in standard display",                                default = 7,          show_default = True)
@click.option('--complete-padding',                 '_cpadding',      type = int,  help = "Padding around cell text in complete display",                  default = 2,          show_default = True)
@click.option('--gutter',                           '_gutter',        type = str,  help = "String delimiting output columns",                              default = '',         show_default = True)
@click.option('--text',                             '_text',          type = str,  help = "Sample text in each cell",                                      default = 'gYw',      show_default = True)
@click.version_option(package_name = 'display-colors')
def main(_standard: bool, _complete: bool, _intensities: str, _reverse_video: bool, _scell_w: int, _cpadding: int, _gutter: str, _text: str) -> None:
	init_mappings()
	intensities = STANDARD_INTENSITIES if _intensities == 'standard' else ALL_INTENSITIES
	if _complete:
		print_all_combinations(intensities, 8, len('XX/XX') + _cpadding, _reverse_video, _gutter)
	if _standard:
		display_theme(intensities, _reverse_video, 8, _text, cell_w = _scell_w, gutter = _gutter)

if __name__ == '__main__':
	main()

# def color_gen_old(colors: tuple[str], offset: int, modifier: Callable) -> Generator[int, int, int]:
# 	for i, color in enumerate(colors):
# 		yield (i + offset, modifier(COLOR_REPR[color]))

# def print_cell_old(fg_attr: int, bg_attr: int, intensity: int, rev_video: bool, str: str, cell_w: int) -> None:
# 	attrs = f'{intensity};{bg_attr};{fg_attr};{REV_VIDEO}' if rev_video else f'{intensity};{fg_attr};{bg_attr}'
# 	print(f"{ANSI_BEG}{attrs}{ANSI_END}{str:^{cell_w}}{ANSI_BEG}{RESET}{ANSI_END}", end = ' ')

# def print_all_combinations_old(intensity: int) -> None:
# 	for   bg_attr, bg_repr in cat_gens(color_gen(('default',), DEFAULT_BG_COLOR_OFFSET, str.lower),
# 																			   color_gen(COLORS,               BG_COLOR_OFFSET, str.lower),
# 																			   color_gen(COLORS,        BRIGHT_BG_COLOR_OFFSET, str.upper),
# 																			  ):
# 		for rev_video in (False, True):
# 			for fg_attr, fg_repr in cat_gens(color_gen(('default',), DEFAULT_FG_COLOR_OFFSET, str.lower),
# 																					color_gen(COLORS,               FG_COLOR_OFFSET, str.lower),
# 																					color_gen(COLORS,        BRIGHT_FG_COLOR_OFFSET, str.upper),
# 																					):
# 				s      = f'{fg_repr}/{bg_repr}'
# 				cell_w = len(s) + 2
# 				print_cell(fg_attr, bg_attr, intensity, rev_video, s, cell_w)
# 			print()

	# print(f'Default/Default:')
	# for intensity in (DIM, MEDIUM, BOLD):
	# 	print_cell_old(DEFAULT_FG, DEFAULT_BG, intensity)
	# print(f'')
	# scr_w = get_terminal_size().columns

	## calculate width of each cell, pass it to print_block()
	## Add 4-bit colors?
	## Can the 4-bit colors vary between terminals?  Can the 8-bit?
	## Test the 4-bit colors 90-97 and 100-107

	# for caption, first, last, cell_w in (("Standard and high-intensity colors", 0, 15, 6),
	# 																		 ("216 colors", 16, 231, 3),
	# 																		 ("Grayscale colors", 232, 255, 5)):
	# 	n_cols = min(36, ((last + 1) - first))
	# 	print(f'{caption}:')
	# 	print_block(first, last, n_cols, cell_w)

# def print_all_combinations_old(intensity: int) -> None:
# 	for   bg_color in cat_gens(color_gen(COLORS,              BG_COLOR_OFFSET),
# 																 color_gen(('default',), DEFAULT_BG_COLOR_OFFSET),
# 																 color_gen(COLORS,       BRIGHT_BG_COLOR_OFFSET)):
# 		for fg_color in cat_gens(color_gen(COLORS,              FG_COLOR_OFFSET),
# 																 color_gen(('default',), DEFAULT_FG_COLOR_OFFSET),
# 																 color_gen(COLORS,       BRIGHT_FG_COLOR_OFFSET)):
# 			print_cell_old(fg_color, bg_color, intensity)
# 		print()

# def print_cell_old(fg_color: int, bg_color: int, intensity: int) -> None:
# 	cell_w = 7
# 	text = f'{fg_color}/{bg_color}'
# 	print(f"{ANSI_BEG}{intensity};{fg_color};{bg_color}{ANSI_END}{text:^{cell_w}}{ANSI_BEG}{RESET}{ANSI_END}", end = '')

# def left_header_old(intensity: str, fg_repr: str) -> str:
# 	str    = f'{intensity} {fg_repr}'
# 	cell_w = len(str) + 2
# 	return f'{str:<{cell_w}}'

# def cell_text_theme_traditional() -> str:
# 	return cell_text(f'gYw')

# def display_theme_old(intensities: list[str], l_col_w: int, cell_txt: str, gutter: str) -> None:
# 	attrs = create_attrs('df', 'df', INTENSITY_ATTR['Default'])
# 	text  = cell_text(text = '', cell_w = l_col_w)
# 	display_cell(attrs, text, gutter)
# 	for bg_repr in cat_gens(color_gen(('default',), str.lower),
# 															color_gen(COLORS,       str.lower),
# 															):
# 		attrs = create_attrs('df', 'df', INTENSITY_ATTR['Default'])
# 		txt   = f'{BG_REPR_ATTR[bg_repr]}m'
# 		text  = cell_text(text = txt, cell_w = len(txt) + 4)
# 		display_cell(attrs, text, gutter)
# 	print()
# 	for fg_repr in cat_gens(color_gen(('default',), str.lower),
# 														  color_gen(COLORS,       str.lower),
# 														 ):
# 		for intensity in intensities:
# 			attrs = create_attrs('df', 'df', INTENSITY_ATTR['Default'])
# 			text  = left_header(intensity, fg_repr, l_col_w)
# 			display_cell(attrs, text, gutter)
# 			for bg_repr in cat_gens(color_gen(('default',), str.lower),
# 																	color_gen(COLORS,       str.lower),
# 																 ):
# 				attrs = create_attrs(fg_repr, bg_repr, INTENSITY_ATTR[intensity])
# 				text = cell_text(text = cell_txt, cell_w = len(cell_txt) + 4)
# 				display_cell(attrs, text, gutter)
# 			print()

# def attrs_all(fg_repr: str, bg_repr: str, intensity:int, rev_video: bool) -> str:
# 	(fg, bg) = (bg_repr, fg_repr) if rev_video else (fg_repr, bg_repr)
# 	return f'{intensity};{FG_REPR_ATTR[fg]};{BG_REPR_ATTR[bg]}' + (f';{REV_VIDEO}' if rev_video else '')

# def cell_text_old(str: str) -> str:
# 	cell_w = len(str) + 2
# 	return f'{str:^{cell_w}}'

