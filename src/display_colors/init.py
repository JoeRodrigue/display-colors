from collections     import namedtuple
from typing          import Callable

from display_colors.const   import (
	_4_BIT_BG_COLOR_OFFSET,
	_4_BIT_BRIGHT_BG_COLOR_OFFSET,
	_4_BIT_BRIGHT_FG_COLOR_OFFSET,
	_4_BIT_DEFAULT_BG_COLOR_OFFSET,
	_4_BIT_DEFAULT_FG_COLOR_OFFSET,
	_4_BIT_FG_COLOR_OFFSET,

	_8_BIT_BG_PREFIX,
	_8_BIT_BG_COLOR_OFFSET,
	_8_BIT_BRIGHT_BG_COLOR_OFFSET,
	_8_BIT_BRIGHT_FG_COLOR_OFFSET,
	_8_BIT_FG_COLOR_OFFSET,
	_8_BIT_FG_PREFIX,
	_8_BIT_GRAYSCALE_N,
	_8_BIT_GRAYSCALE_OFFSET,
	_8_BIT_PALETTE_N,
	_8_BIT_PALETTE_OFFSET,
	_8_BIT_STANDARD_N,
	_8_BIT_STANDARD_OFFSET,

	COLORS,
	COLOR_REPR,
)

_4_BIT_BG_REPR_ATTR  = dict()
_4_BIT_FG_REPR_ATTR  = dict()
_8_BIT_BG_REPR_ATTR  = dict()
_8_BIT_FG_REPR_ATTR  = dict()

Switch_Attr = namedtuple('Switch_Attr', ['on', 'off',],)

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
	def init_mapping(target: dict[str, str], colors: tuple[str], offset: int, modifier: Callable, prefix: str) -> None:
		for code, color in enumerate(colors, start = offset):
			target[modifier(COLOR_REPR[color])] = f'{prefix}{code}'

	def init_palette(target: dict[str, str], n: int, offset: int, prefix: str) -> None:
		for code in range(offset, offset + n):
			target[str(code)] = f'{prefix}{code}'

	for target, colors, offset, modifier, prefix in (
		(_4_BIT_FG_REPR_ATTR, COLORS,               _4_BIT_FG_COLOR_OFFSET, str.lower, ''),
		(_4_BIT_FG_REPR_ATTR, ('default',), _4_BIT_DEFAULT_FG_COLOR_OFFSET, str.lower, ''),
		(_4_BIT_FG_REPR_ATTR, COLORS,        _4_BIT_BRIGHT_FG_COLOR_OFFSET, str.upper, ''),
		(_4_BIT_BG_REPR_ATTR, COLORS,               _4_BIT_BG_COLOR_OFFSET, str.lower, ''),
		(_4_BIT_BG_REPR_ATTR, ('default',), _4_BIT_DEFAULT_BG_COLOR_OFFSET, str.lower, ''),
		(_4_BIT_BG_REPR_ATTR, COLORS,        _4_BIT_BRIGHT_BG_COLOR_OFFSET, str.upper, ''),

		(_8_BIT_FG_REPR_ATTR, COLORS,               _8_BIT_FG_COLOR_OFFSET, str.lower, _8_BIT_FG_PREFIX),
		(_8_BIT_FG_REPR_ATTR, COLORS,        _8_BIT_BRIGHT_FG_COLOR_OFFSET, str.upper, _8_BIT_FG_PREFIX),
		(_8_BIT_BG_REPR_ATTR, COLORS,               _8_BIT_BG_COLOR_OFFSET, str.lower, _8_BIT_BG_PREFIX),
		(_8_BIT_BG_REPR_ATTR, COLORS,        _8_BIT_BRIGHT_BG_COLOR_OFFSET, str.upper, _8_BIT_BG_PREFIX),
	):
		init_mapping(target, colors, offset, modifier, prefix)

	for target, n, offset, prefix in (
		(_8_BIT_BG_REPR_ATTR, _8_BIT_STANDARD_N,  _8_BIT_STANDARD_OFFSET,  _8_BIT_BG_PREFIX),
		(_8_BIT_BG_REPR_ATTR, _8_BIT_PALETTE_N,   _8_BIT_PALETTE_OFFSET,   _8_BIT_BG_PREFIX),
		(_8_BIT_BG_REPR_ATTR, _8_BIT_GRAYSCALE_N, _8_BIT_GRAYSCALE_OFFSET, _8_BIT_BG_PREFIX),
		(_8_BIT_FG_REPR_ATTR, _8_BIT_STANDARD_N,  _8_BIT_STANDARD_OFFSET,  _8_BIT_FG_PREFIX),
		(_8_BIT_FG_REPR_ATTR, _8_BIT_PALETTE_N,   _8_BIT_PALETTE_OFFSET,   _8_BIT_FG_PREFIX),
		(_8_BIT_FG_REPR_ATTR, _8_BIT_GRAYSCALE_N, _8_BIT_GRAYSCALE_OFFSET, _8_BIT_FG_PREFIX),
	):
		init_palette(target, n, offset, prefix)

