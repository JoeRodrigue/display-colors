from typing import NamedTuple

SGR_BEG   = '\033['
SGR_END   = 'm'
RESET     = '0'
DIM       = '2'
MEDIUM    = '22'
ITALIC    = '3'
BOLD      = '1'
REV_VIDEO = '7'
UNDERLINE = '4'

_8_BIT_FG_PREFIX = '38;5;'
_8_BIT_BG_PREFIX = '48;5;'

CODE_COL_WIDTH = 8       ## Widest attr code is '22;97;7m'

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

_4_BIT_FG_COLOR_OFFSET         = 30
_4_BIT_BG_COLOR_OFFSET         = 40
_4_BIT_BRIGHT_FG_COLOR_OFFSET  = 90
_4_BIT_BRIGHT_BG_COLOR_OFFSET  = 100

_4_BIT_DEFAULT_FG_COLOR_OFFSET = 39
_4_BIT_DEFAULT_BG_COLOR_OFFSET = 49

_8_BIT_FG_COLOR_OFFSET         = 0
_8_BIT_BG_COLOR_OFFSET         = 0
_8_BIT_BRIGHT_FG_COLOR_OFFSET  = 8
_8_BIT_BRIGHT_BG_COLOR_OFFSET  = 8

_8_BIT_PALETTE_CUBE_SIDE = 6

_8_BIT_COLORS_N          = 2 ** 8
_8_BIT_STANDARD_N        = 2 * len(COLORS)
_8_BIT_PALETTE_N         = _8_BIT_PALETTE_CUBE_SIDE ** 3
_8_BIT_GRAYSCALE_N       = _8_BIT_COLORS_N - _8_BIT_STANDARD_N - _8_BIT_PALETTE_N

_8_BIT_STANDARD_OFFSET   = 0
_8_BIT_PALETTE_OFFSET    = _8_BIT_STANDARD_OFFSET + _8_BIT_STANDARD_N
_8_BIT_GRAYSCALE_OFFSET  = _8_BIT_PALETTE_OFFSET  + _8_BIT_PALETTE_N

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

class Switch_Attr(NamedTuple):
	"""Store attributes that switch a property on and off"""
	on:  str
	off: str
