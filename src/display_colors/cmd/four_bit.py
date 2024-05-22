import click
from collections.abc import Generator

from display_colors.cell import (
	cell_text,
	colored_cell,
	create_attrs,
)
from display_colors.const import (
	ALL_WEIGHTS,
	CODE_COL_WIDTH,
	COLOR_REPR,
	COLORS,
	REV_VIDEO,
	WEIGHT_ATTR,
	WEIGHT_REPR,
)
from display_colors.gen import (
	cat_gens,
)
from display_colors.init import (
	_4_BIT_BG_REPR_ATTR,
	_4_BIT_FG_REPR_ATTR,
)

def blank_cell(cell_w: int) -> str:
	return colored_cell(create_attrs('Default', 'df', 'df'), f'{"":{cell_w}}')

def fg_attr_repr(weight: str, fg_repr: str, rev_video: bool, cell_w: int) -> str:
	rv_attr = f';{REV_VIDEO}' if rev_video else ''
	str     = f'{WEIGHT_ATTR[weight]};{_4_BIT_FG_REPR_ATTR[fg_repr]}{rv_attr}m'
	return f'{str:>{cell_w}}'

def fg_col_gen(weights: list[str], reverse_video: bool, stanzas: bool) -> Generator[str, str, str]:
	col_w = len(COLOR_REPR['default'])
	yield blank_cell(col_w)
	prefix = f''
	for fg_repr in cat_gens(
		map(lambda color: COLOR_REPR[color].lower(), ('default',)),
		map(lambda color: COLOR_REPR[color].lower(), COLORS),
		map(lambda color: COLOR_REPR[color].upper(), COLORS),
	):
		new_stanza = True
		for _ in weights:
			for _ in (False, True) if reverse_video else (False,):
				attrs = create_attrs('Default', 'df', 'df')
				text = f'{prefix}{fg_repr}'
				yield colored_cell(attrs, text) if new_stanza else blank_cell(col_w)
				new_stanza = False
		prefix = f'\n' if stanzas else f''

def weight_col_gen(weights: list[str], reverse_video: bool, header: bool = False) -> Generator[str, str, str]:
	if header:
		yield blank_cell(len(WEIGHT_REPR['Default']))
	for _ in cat_gens(map(lambda color: COLOR_REPR[color].lower(), ('default',)),
										map(lambda color: COLOR_REPR[color].lower(), COLORS),
										map(lambda color: COLOR_REPR[color].upper(), COLORS),
	):
		for weight in weights:
			for rev_video in (False, True) if reverse_video else (False,):
				attrs = create_attrs('Default', 'df', 'df', rev_video = rev_video)
				text  = f'{WEIGHT_REPR[weight]}'
				yield colored_cell(attrs, text)

def code_col_gen(weights: list[str], reverse_video: bool, col_w: int) -> Generator[str, str, str]:
	yield blank_cell(col_w)
	for fg_repr in cat_gens(map(lambda color: COLOR_REPR[color].lower(), ('default',)),
												  map(lambda color: COLOR_REPR[color].lower(), COLORS),
													map(lambda color: COLOR_REPR[color].upper(), COLORS),
	):
		for weight in weights:
			for rev_video in (False, True) if reverse_video else (False,):
				attrs = create_attrs('Default', 'df', 'df')
				text  = fg_attr_repr(weight, fg_repr, rev_video, col_w)
				yield colored_cell(attrs, text)

def column_gen(bg_repr: str, weights: list[str], reverse_video: bool, cell_txt: str, col_w: int, transpose: bool) -> Generator[str, str, str]:
	if not transpose:
		attrs = create_attrs('Default', 'df', 'df')
		text  = cell_text(text = f'{_4_BIT_BG_REPR_ATTR[bg_repr]}m', cell_w = col_w)
		yield colored_cell(attrs, text)
	for fg_repr in cat_gens(map(lambda color: COLOR_REPR[color].lower(), ('default',)),
												  map(lambda color: COLOR_REPR[color].lower(), COLORS),
													map(lambda color: COLOR_REPR[color].upper(), COLORS),
	):
		(fg, bg) = (bg_repr, fg_repr) if transpose else (fg_repr, bg_repr)
		for weight in weights:
			for rev_video in (False, True) if reverse_video else (False,):
				attrs = create_attrs(weight, fg, bg, rev_video = rev_video)
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
				 for bg_repr in cat_gens(map(lambda color: COLOR_REPR[color].lower(), ('default',)),
														 		 map(lambda color: COLOR_REPR[color].lower(), COLORS),
																 map(lambda color: COLOR_REPR[color].upper(), COLORS),
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

@click.command('4-bit')
@click.option('--col-width',     '_col_w',        type = int,  help = "Column width",                                                  default = 7,     show_default = True)
@click.option('--gutter',        '_gutter',       type = str,  help = "String delimiting output columns  [default: empty string]",     default = '',    show_default = True)
@click.option('--reverse-video', '_rev_video', is_flag = True, help = "Add 'background-color on foreground-color' in reverse video",   default = False, show_default = True)
@click.option('--stanzas',       '_stanzas',   is_flag = True, help = "Group output rows by color (non-transposed only)",              default = False, show_default = True)
@click.option('--text',          '_text',         type = str,  help = "Sample text in each cell (non-transposed only)",                default = 'gYw', show_default = True)
@click.option('--transpose',     '_transpose', is_flag = True, help = "Display foreground colors in column-major order  [default: row-major order]", default = False, show_default = True)
@click.option('--weight', '-w',  '_weights',      type = click.Choice(['dim', 'default', 'medium', 'bold', 'all'], case_sensitive = False), multiple = True, help = "Which weight font to display (use multiple times)", default = ['default', 'bold'], show_default = True)
def display_4_bit(_weights: list[str], _rev_video: bool, _col_w: int, _gutter: str, _stanzas: bool, _text: str, _transpose: bool):
	"""All combinations (FG on BG) of the 16 standard 4-bit colors"""
	weights = ALL_WEIGHTS if 'all' in _weights else [w.capitalize() for w in _weights]
	display_theme(weights, _rev_video, _text, col_w = _col_w, gutter = _gutter, stanzas = _stanzas, transpose = _transpose)
