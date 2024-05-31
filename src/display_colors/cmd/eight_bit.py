import click
from collections     import namedtuple
from functools       import partial

from display_colors.cell  import (
	cell_text,
	colored_cell,
)
from display_colors.const import (
	_8_BIT_GRAYSCALE_N,
	_8_BIT_GRAYSCALE_OFFSET,
	_8_BIT_PALETTE_CUBE_SIDE,
	_8_BIT_PALETTE_OFFSET,
	_8_BIT_STANDARD_N,
	_8_BIT_STANDARD_OFFSET,
	COLOR_REPR,
	COLORS,
)
from display_colors.init import (
	_4_BIT_BG_REPR_ATTR,
	_4_BIT_FG_REPR_ATTR,
	_8_BIT_BG_REPR_ATTR,
	_8_BIT_FG_REPR_ATTR,
)
from display_colors.math import (
	base_n_10,
)

Point = namedtuple('Point', ['x', 'y', 'z'])

def p_disc_fgattr(p: Point, discriminant: callable, _4_bit = False) -> str:
	(color, modifier) = ('black', str.lower) if discriminant(p) else ('white', str.upper)
	repr = modifier(COLOR_REPR[color])
	return _4_BIT_FG_REPR_ATTR[repr]if _4_bit else _8_BIT_FG_REPR_ATTR[repr]

def p_code_bgattr(p: Point, p_code: callable, _4_bit = False) -> str:
	if _4_bit:
		code     = p_code(p) - _8_BIT_STANDARD_OFFSET
		color    = COLORS[code % len(COLORS)]
		modifier = str.upper if code // len(COLORS) else str.lower
		repr     = modifier(COLOR_REPR[color])
		return _4_BIT_BG_REPR_ATTR[repr]
	return _8_BIT_BG_REPR_ATTR[str(p_code(p))]

def p_code_text(p: Point, p_code: callable, decimal: bool) -> str:
	fmt_spec = 'd' if decimal else 'X'
	return f'{p_code(p):{fmt_spec}}'

def display_standard(p_code: callable, cell_w: int, decimal: bool) -> None:
	def discriminant(p: Point) -> bool:
		delta = p_code(p) - _8_BIT_STANDARD_OFFSET
		return bool((delta // (_8_BIT_STANDARD_N / 2)) % 2)

	dimensions = Point(_8_BIT_STANDARD_N, 1, 1)
	print('8-bit', end = ' ')
	display_cuboid(dimensions,
								partial(p_disc_fgattr, discriminant = discriminant),
								partial(p_code_bgattr, p_code       = p_code),
								partial(p_code_text,   p_code       = p_code, decimal = decimal),
								cell_w)
	print('4-bit', end = ' ')
	display_cuboid(dimensions,
								partial(p_disc_fgattr, discriminant = discriminant, _4_bit = True),
								partial(p_code_bgattr, p_code       = p_code,       _4_bit = True),
								partial(p_code_text,   p_code       = p_code, decimal = decimal),
								cell_w)

def display_rgb_palette(p_code: callable, cell_w: int, decimal: bool) -> None:
	def discriminant(p: Point) -> bool:
		delta = p_code(p) - _8_BIT_PALETTE_OFFSET
		return bool((delta // (_8_BIT_PALETTE_CUBE_SIDE * _8_BIT_PALETTE_CUBE_SIDE / 2)) % 2)

	dimensions = Point(_8_BIT_PALETTE_CUBE_SIDE, _8_BIT_PALETTE_CUBE_SIDE, _8_BIT_PALETTE_CUBE_SIDE)
	display_cuboid(dimensions,
								partial(p_disc_fgattr, discriminant = discriminant),
								partial(p_code_bgattr, p_code       = p_code),
								partial(p_code_text,   p_code       = p_code, decimal = decimal),
								cell_w)

def display_grayscale(p_code: callable, cell_w: int, decimal: bool) -> None:
	def discriminant(p: Point) -> bool:
		delta = p_code(p) - _8_BIT_GRAYSCALE_OFFSET
		return bool((delta // (_8_BIT_GRAYSCALE_N / 2)) % 2)

	dimensions = Point(_8_BIT_GRAYSCALE_N, 1, 1)
	display_cuboid(dimensions,
								partial(p_disc_fgattr, discriminant = discriminant),
								partial(p_code_bgattr, p_code       = p_code),
								partial(p_code_text,   p_code       = p_code, decimal = decimal),
								cell_w)

def display_cuboid(dimensions: Point, p_fgattr: callable, p_bgattr: callable, f_text: callable, cell_w: int) -> None:
	for y in range(dimensions.y):
		for z in range(dimensions.z):
			for x in range(dimensions.x):
				p = Point(x, y, z)
				text = cell_text(text = f_text(p), cell_w = cell_w)
				print(colored_cell(f'{p_fgattr(p)};{p_bgattr(p)}', text), end  = '')
			print(' ', end = '')
		print()

@click.command('8-bit')
@click.option('--std-col-width', '_std_col_w', type = int, help = "Standard color cell width", default = 7, show_default = True)
@click.option('--rgb-col-width', '_rgb_col_w', type = int, help = "RGB color cell width", default = 3, show_default = True)
@click.option('--gray-col-width', '_gray_col_w', type = int, help = "Grayscale cell width", default = 5, show_default = True)
@click.option('--decimal',        '_decimal', is_flag = True, help = "Display color codes in decimal  [default: hex]", default = False, show_default = True)
def display_8_bit(_std_col_w: int, _rgb_col_w: int, _gray_col_w: int, _decimal: bool) -> None:
	"""The 16 standard colors, the RGB 6x6x6 palette, and 24 grays (BG)"""
	for title, p_code in (
		('Standard and bright colors:', lambda p: p.x - _8_BIT_STANDARD_OFFSET),
	):
		print(title)
		display_standard(p_code, _std_col_w, _decimal)

	for title, p_code in (
		('RGB palette cube, front:', lambda p: base_n_10(_8_BIT_PALETTE_CUBE_SIDE, p.x, p.y, p.z) + _8_BIT_PALETTE_OFFSET),
		('Top:',                     lambda p: base_n_10(_8_BIT_PALETTE_CUBE_SIDE, p.x, p.z, p.y) + _8_BIT_PALETTE_OFFSET),
		('Left side:',               lambda p: base_n_10(_8_BIT_PALETTE_CUBE_SIDE, p.z, p.y, p.x) + _8_BIT_PALETTE_OFFSET),
	):
		print(title)
		display_rgb_palette(p_code, _rgb_col_w, _decimal)

	for title, p_code in (
		('Grayscale:', lambda p: p.x + _8_BIT_GRAYSCALE_OFFSET),
	):
		print(title)
		display_grayscale(p_code, _gray_col_w, _decimal)
